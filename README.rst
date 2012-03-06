tw2.jit
=======

:Author: Ralph Bean <rbean@redhat.com>

.. figure:: tw2.jit/raw/master/doc/images/screenshot1.png
    :alt: An examle of the RadialGraph widget
    :target: http://github.com/toscawidgets/tw2.jit
    :align: center

    A screenshot of the ``tw2.jit.widgets.RadialGraph`` widget in action.
    Its crazy interactive when its not just a screenshot!

.. comment: split here

.. _toscawidgets2 (tw2): http://toscawidgets.org/documentation/tw2.core/
.. _thejit: http://thejit.org

tw2.jit is a `toscawidgets2 (tw2)`_ wrapper for `thejit`_.

Live Demo
---------

Peep the `live demonstration <http://tw2-demos.threebean.org/module?module=tw2.jit>`_ and
`screenshots <http://github.com/toscawidgets/tw2.jit/raw/master/doc/images/screenshot1.png>`_.

Links
-----

You can `get the source from github <http://github.com/toscawidgets/tw2.jit>`_,
check out `the PyPI page <http://pypi.python.org/pypi/tw2.jit>`_, and
report or look into `bugs <http://github.com/toscawidgets/tw2.jit/issues/>`_.

Description
-----------

`toscawidgets2 (tw2)`_ aims to be a practical and useful widgets framework
that helps people build interactive websites with compelling features, faster
and easier. Widgets are re-usable web components that can include a template,
server-side code and JavaScripts/CSS resources. The library aims to be:
flexible, reliable, documented, performant, and as simple as possible.

The JavaScript InfoVis Toolkit (`thejit`_) is a javascript library that
provides web standard based tools to create interactive data visualizations
for the Web.  It is pretty, interactive, and fast.

This module, tw2.jit, provides `toscawidgets2 (tw2)`_ widgets that render `thejit`_ data visualizations.

Sampling tw2.jit in the WidgetBrowser
-------------------------------------

The best way to scope out ``tw2.jit`` is to load its widgets in the
``tw2.devtools`` WidgetBrowser.  To see the source code that configures them,
check out ``tw2.jit/tw2/jit/samples.py``

To give it a try you'll need git, python, and `virtualenvwrapper
<http://pypi.python.org/pypi/virtualenvwrapper>`_.  Run::

    $ git clone git://github.com/toscawidgets/tw2.jit.git
    $ cd tw2.jit
    $ mkvirtualenv tw2.jit
    (tw2.jit) $ pip install tw2.devtools
    (tw2.jit) $ python setup.py develop
    (tw2.jit) $ paster tw2.browser

...and browse to http://localhost:8000/ to check it out.
