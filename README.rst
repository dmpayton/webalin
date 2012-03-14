webalin
=======

**Web** **A**\ ccessibility **Lin**\ ter

:Author: `Derek Payton`_
:License: MIT

Dependencies
------------

* `lxml`_
* `requests`_
* JSON of some sort (json, simplejson, or django.utils.simplejson)

Install
-------

*Forthcoming...*

Usage
-----

**Library**::

    >>> import webalin
    >>> webalin.analyze('https://www.djangoproject.com/')
    { ... }
    >>> webalin.analyze(open('document.html', 'r').read())
    { ... }

**Command Line**::

    $ webalin http://www.python.org
    ...
    $ cat document.html | webalin
    ...

.. _Derek Payton: http://dmpayton.com
.. _lxml: http://lxml.de/
.. _requests: http://python-requests.org/