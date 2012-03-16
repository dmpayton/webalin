webalin
=======

**Web** **A**\ ccessibility **Lin**\ ter

:Author: `Derek Payton`_
:License: MIT

Dependencies
------------

* `lxml`_
* `requests`_
* JSON library (`json`_, `simplejson`_, or `django.utils.simplejson`_)

Install
-------

*Forthcoming...*

Usage
-----

**Library**


``webalin.analyze`` can accept a URL or a full HTML document and returns errors
as a list::

    >>> import webalin
    >>> webalin.analyze('https://www.djangoproject.com/')
    [ ... ]
    >>> webalin.analyze(open('document.html', 'r').read())
    [ ... ]

**Command Line**

The command line utility accepts arguments from ``sys.stdin`` or ``sys.argv``
and prints errors to stdout::

    $ webalin http://www.python.org
    ...
    $ cat document.html | webalin
    ...

**Output Sample**

Format: ``[type]: [lineno]: [message]``

::

    E: -: <!DOCTYPE> is missing
    E: -: <title> is missing
    E: 7: <img:/satic/images/logo.png> is missing [alt]
    E: 17: <table> is missing [summary]
    E: 19: <th> is missing [scope]
    E: 20: <th> is missing [scope]
    E: 37: <input:id_username> is missing <label>
    E: 41: <input:id_password> is missing <label>
    W: 17: <table> contains no <tr> with [scope]



.. _Derek Payton: http://dmpayton.com
.. _lxml: http://lxml.de/
.. _requests: http://python-requests.org/
.. _json: http://docs.python.org/library/json.html
.. _simplejson: http://pypi.python.org/pypi/simplejson/
.. _django.utils.simplejson: https://www.djangoproject.com/
