webalin
=======

`Webalin`_ is a **Web** **A**\ ccessibility **Lin**\ ter that helps determine
if a given HTML document is `Section 508`_ compliant.

:Author: `Derek Payton`_
:Version: 0.1.0-dev
:License: `MIT`_

Documentation
-------------

http://webalin.readthedocs.org/

tl;dr
~~~~~

::

    $ pip install -e git+git://github.com/dmpayton/webalin.git
    ...
    $ webalin http://python.org
    E: 94: <input:domains> is missing <label>
    E: 95: <input:sitesearch> is missing <label>
    E: 96: <input:sourceid> is missing <label>
    E: 97: <input:q> is missing <label>
    E: 200: <input> is missing [id]

.. _Webalin: https://github.com/dmpayton/webalin
.. _Derek Payton: http://dmpayton.com
.. _MIT: https://github.com/dmpayton/webalin/blob/master/LICENSE
.. _Section 508: http://section508.gov