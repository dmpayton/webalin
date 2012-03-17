#!/usr/bin/env python

import lxml.html
import requests
import warnings
from operator import itemgetter


class HttpStatusWarning(Warning):
    pass


class LintMessages(object):
    def __init__(self):
        self._log = []
        self._stats = {
            'warnings': 0,
            'errors': 0
            }

    def log(self, message, level, element=None):
        lineno = getattr(element, 'sourceline', None)
        self._log.append((level, lineno, message))

    def get_output(self):
        output = {
            'messages': [],
            'stats': self._stats
            }
        logs = sorted(self._log, key=itemgetter(0, 1))
        for level, lineno, message in logs:
            lineno = lineno or '-'
            output['messages'].append('{0}: {1}: {2}'.format(level, lineno, message))
        return output

    def warn(self, message, element=None):
        self.log(message, 'W', element)
        self._stats['warnings'] += 1

    def error(self, message, element=None):
        self.log(message, 'E', element)
        self._stats['errors'] += 1


class Webalin(object):
    def __init__(self):
        self.markup = None
        self.dom = None
        self.log = LintMessages()

    def analyze(self, markup_or_url, tests=None):
        ''' Parse and test an HTML document '''
        if markup_or_url.startswith('http'):
            self.load_url(markup_or_url)
        else:
            self.load_markup(markup_or_url)

        ## Determine which tests to run
        if tests is None:
            tests = [x[6:] for x in dir(self) if x.startswith('check_')]

        ## Run our tests
        for method in tests:
            try:
                getattr(self, 'check_{0}'.format(method))()
            except AttributeError:
                self.log.error('Skipped non-existent test [{0}]'.format(method))

        ## Sort messages by lineno and return
        return self.log.get_output()

    def load_url(self, url):
        ''' Fetch a URL and load the markup '''
        r = requests.get(url)
        if r.status_code != 200:
            warnings.warn('URL <{0}> returned non-200 response'.format(url), HttpStatusWarning)
        self.load_markup(r.content)

    def load_markup(self, markup):
        ''' Parse an HTML document with lxml '''
        self.markup = markup
        self.dom = lxml.html.document_fromstring(markup)

    def verify_attribute(self, element, attr, identifier=None, required=True):
        ''' Check that a given element contains a specific attribute '''
        ## Format the elements display fo output
        display = element.tag
        if identifier:
            display = '{0}:{1}'.format(element.tag, identifier)

        ## Test for the attributes existence
        value = element.get(attr)
        if value is None:
            ## Attribute is completely missing
            self.log.error('<{0}> is missing [{1}]'.format(display, attr), element)
            return False
        elif (not value) and required:
            ## Attribute is empty and required
            self.log.error('<{0}> has empty [{1}]'.format(display, attr), element)
            return False
        return True

    ## Accessibility tests

    def check_doctype(self):
        ''' The document must specify <!DOCTYPE> '''
        if not self.markup.strip().startswith('<!DOCTYPE'):
            self.log.error('<!DOCTYPE> is missing')

    def check_title(self):
        ''' <title> must exist '''
        try:
            title = self.dom.cssselect('title')[0]
        except IndexError:
            self.log.error('<title> is missing')
            return
        if not title.text:
            self.log.error('<title> is empty', title)

    def check_img_alt(self):
        ''' <img> must specify [alt] '''
        for img in self.dom.cssselect('img'):
            self.verify_attribute(img, 'alt', img.get('src'), False)

    def check_img_map_area_alt(self):
        ''' <area>'s for <img[usemap]> must specify [alt] '''
        for img in self.dom.cssselect('img[usemap]'):
            usemap = img.get('usemap').lstrip('#')
            for area in self.dom.cssselect('map[name="{0}"] area'.format(usemap)):
                self.verify_attribute(area, 'alt', usemap)

    def check_input_image_alt(self):
        ''' <input[type="image"]> must specify [alt] '''
        for button in self.dom.cssselect('input[type=image]'):
            self.verify_attribute(button, 'alt', button.get('src'))

    def check_input_label(self):
        ''' <form> elements must have <label>s '''
        no_label_required = ('button', 'submit', 'reset', 'image')
        for input in self.dom.cssselect('input, textarea, select'):
            if input.tag == 'input' and input.get('type') in no_label_required:
                ## Buttons don't need explicit labels, do they?
                continue

            ## An id attribute is a requirement for labels
            input_id = input.get('id')
            if not input_id:
                self.log.error('<{0}> is missing [id]'.format(input.tag), input)
                return

            ## Ensure we have a matching non-empty label tag
            try:
                label = self.dom.cssselect('label[for="{0}"]'.format(input_id))[0]
                if not label.text:
                    self.log.error('<label:{0}]> is empty'.format(input_id), label)
            except IndexError:
                self.log.error('<{0}:{1}> is missing <label>'.format(input.tag, input_id), input)

    def check_table_summary(self):
        ''' <table> must specify [summary] '''
        for table in self.dom.cssselect('table'):
            summary = table.get('summary')
            if summary is None:
                self.log.error('<table> is missing [summary]', table)
            elif not summary:
                self.log.error('<table> has empty [summary]', table)

    def check_table_scope(self):
        ''' <th> and <tr> should specify [scope] '''
        for table in self.dom.cssselect('table'):
            ## <th>'s need a scope
            for th in table.cssselect('th'):
                self.verify_attribute(th, 'scope')

            rows = table.cssselect('tr[scope]')
            if not len(rows):
                self.log.warn('<table> contains no <tr> with [scope]', table)


def analyze(markup_or_url, tests=None):
    ''' Analyze a document or URL and return the statistics '''
    w = Webalin()
    return w.analyze(markup_or_url, tests)
