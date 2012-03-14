#!/usr/bin/env python

import html5lib
import lxml.html
import requests
import warnings


class HttpStatusWarning(Warning):
    pass


class ErrorMessages(object):
    def __init__(self):
        self.messages = []

    def log(self, message, element=None, level=None):
        level = level or 'D'
        lineno = getattr(element, 'sourceline', '-')
        message = '{0}: {1}: {2}'.format(lineno, level, message)
        self.messages.append(message)

    def warning(self, message, element=None):
        self.log(message, element, 'W')

    def error(self, message, element=None):
        self.log(message, element, 'E')


class Webalin(object):
    def __init__(self):
        self.markup = None
        self.dom = None
        self.stats = {} # arbitrary info
        self.log = ErrorMessages()

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

    def analyze(self, markup_or_url):
        ''' Parse and test an HTML document '''
        if markup_or_url.startswith('http'):
            self.load_url(markup_or_url)
        else:
            self.load_markup(markup_or_url)

        ## Run our tests
        tests = [x for x in dir(self) if x.startswith('check_')]
        for method in tests:
            getattr(self, method)()

        ## Return stats and messages
        return {
            'stats': self.stats,
            'messages': sorted(self.log.messages) # sort by lineno
            }

    ## Accessability tests

    def check_title(self):
        ''' The title tag exists and has content '''
        try:
            title = self.dom.cssselect('title')[0]
        except IndexError:
            self.log.error('Missing <title>')
            return
        if not title.text:
            self.log.error('<title> is empty', title)

    def check_images(self):
        ''' All img tags have alt attributes '''
        for img in self.dom.cssselect('img'):
            alt = img.get('alt')
            if alt is None:
                ## alt not present
                self.log.error('<img:{0}> missing alt attribute'.format(img.get('src')), img)
            elif not alt:
                ## alt is empty
                self.log.warning('<img:{0}> empty alt attribute'.format(img.get('src')), img)

    def check_image_buttons(self):
        ''' All inputs of type="image" specify an alt attribute '''
        for button in self.dom.cssselect('input[type=image]'):
            ## alt is absolutely required
            if not button.get('alt'):
                self.log.error('<input:{0}> missing alt attribute'.format(button.get('src')), button)


def analyze(markup_or_url):
    ''' Analyze a document or URL and return the statistics '''
    w = Webalin()
    return w.analyze(markup_or_url)
