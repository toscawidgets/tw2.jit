tw2.jit
=======

:Author: Ralph Bean <ralph.bean@gmail.com>

.. figure:: tw2.jit/raw/master/doc/images/screenshot1.png
    :alt: An examle of the RadialGraph widget
    :target: http://github.com/ralphbean/tw2.jit
    :align: center

    A screenshot of the ``tw2.jit.widgets.RadialGraph`` widget in action.
    Its crazy interactive when its not just a screenshot!

.. comment: split here

.. _toscawidgets2 (tw2): http://toscawidgets.org/documentation/tw2.core/
.. _thejit: http://thejit.org

tw2.jit is a `toscawidgets2 (tw2)`_ wrapper for `thejit`_.

`Screenshots <http://github.com/ralphbean/tw2.jit/raw/master/doc/images/screenshot1.png>`_

`Bugs <http://github.com/ralphbean/tw2.jit/issues/>`_

Sampling tw2.jit in the WidgetBrowser
-------------------------------------

The best way to scope out ``tw2.jit`` is to load its widgets in the 
``tw2.devtools`` WidgetBrowser.  To see the source code that configures them,
check out ``tw2.jit.samples``

To give it a try you'll need git, mercurial, python, and virtualenv.  Run:

    ``git clone git://github.com/ralphbean/tw2.jit.git``

    ``cd tw2.jit``

The following script will set up all the necessary tw2 dependencies in a
python virtualenv:

    ``./develop-tw2-destroy-and-setup.sh``

The following will enter the virtualenv and start up ``paster tw2.browser``:

    ``./develop-tw2-start.sh``

...and browse to http://localhost:8000/ to check it out.



