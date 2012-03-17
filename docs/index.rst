Webalin: Section 508 Compliance Linter
======================================

`Webalin`_ is a **Web** **A**\ ccessibility **Lin**\ ter that helps ensure
your website is `Section 508`_ compliant. Webalin is written in Python and
can be called from the command line or imported for use in your projects test
suite.

:Author: `Derek Payton`_
:Version: 0.1.0
:License: `MIT`_

A Quick Demo
------------

::

    $ webalin http://python.org
    E: 94: <input:domains> is missing <label>
    E: 95: <input:sitesearch> is missing <label>
    E: 96: <input:sourceid> is missing <label>
    E: 97: <input:q> is missing <label>
    E: 200: <input> is missing [id]


Contents
--------

.. toctree::
    :maxdepth: 2

    manual/install
    manual/usage
    manual/testing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Webalin: https://github.com/dmpayton/webalin
.. _Derek Payton: http://dmpayton.com
.. _MIT: https://github.com/dmpayton/webalin/blob/master/LICENSE
.. _Section 508: http://section508.gov
