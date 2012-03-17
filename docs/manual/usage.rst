Usage
=====

Library
-------

``webalin.analyze`` can accept a URL or a full HTML document and returns errors
as a list::

    >>> import webalin
    >>> webalin.analyze('https://python.org/')
    {'messages': ['E: 94: <input:domains> is missing <label>',
                  'E: 95: <input:sitesearch> is missing <label>',
                  'E: 96: <input:sourceid> is missing <label>',
                  'E: 97: <input:q> is missing <label>',
                  'E: 200: <input> is missing [id]'],
     'stats': {'errors': 5, 'warnings': 0}}

    >>> webalin.analyze(open('accessible-document.html', 'r').read())
    {'messages': [], 'stats': {'errors': 0, 'warnings': 0}}

Command Line
------------

The command line utility accepts arguments from ``sys.stdin`` or ``sys.argv``
and prints errors to stdout::

    $ ./webalin https://www.djangoproject.com

    $ cat tests/resources/inaccessible.html | ./webalin
    E: -: <!DOCTYPE> is missing
    E: -: <title> is missing
    E: 7: <img:/satic/images/logo.png> is missing [alt]
    E: 17: <table> is missing [summary]
    E: 19: <th> is missing [scope]
    E: 20: <th> is missing [scope]
    E: 37: <input:id_username> is missing <label>
    E: 41: <input:id_password> is missing <label>
    W: 17: <table> contains no <tr> with [scope]
