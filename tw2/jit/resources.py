""" Special tw2.jit resource types """

import weakref
import types

import tw2.core as twc

from tw2.core.resources import JSSource

class CompoundJSSource(JSSource):
    """ Takes multiple JSSource/JSFuncCall params and displays them
    all within the same <script> tag and javascript scope.

    Used by tw2.jit to separate the namespaces of different widgets on the
    same page.  widget variable names (like ``var jitwidget``) can be shared
    between different calls of a certain widget, but not come into conflict
    with other widgets.
    """

    children = twc.Param('An iterable of twc.JSSource objects')
    exec_delay = twc.Param('Value in milliseconds to delay execution',default=0)
    src = None
    location = 'bodybottom'

    @classmethod
    def post_define(cls):
        """
        1) Check children are valid
        2) Disable their 'display' method
        3) Update them to have a parent link.
        """

        cls._sub_compound = not getattr(cls, 'id', None)
        if not hasattr(cls, 'children'):
            return
        joined_cld = []
        for c in cls.children:
            if not isinstance(c, type) or not issubclass(c, JSSource):
                raise twc.ParameterError("Children must be JSSources")
            # Override children's display method so they don't go
            #  rendering on their own.  We want to aggregate their
            #  sources into our own wrapped js call.
            class DisabledJSSource(c):
                def display(self, displays_on):
                    return ''
            joined_cld.append(DisabledJSSource(parent=cls))
        ids = set()
        for c in cls.children_deep():
            if getattr(c, 'id', None):
                if c.id in ids:
                    raise twc.WidgetError("Duplicate id %s" % c.id)
                ids.add(c.id)

        cls.children = twc.widgets.WidgetBunch(joined_cld)

    def __init__(self, **kw):
        super(CompoundJSSource, self).__init__(**kw)
        self.children = twc.widgets.WidgetBunch(
            c.req(parent=weakref.proxy(self)) for c in self.children)

    @classmethod
    def children_deep(cls):
        if getattr(cls, 'id', None):
            yield cls
        else:
            for c in getattr(cls, 'children', []):
                for cc in c.children_deep():
                    yield cc

    def prepare(self):
        if not self.src:
            for c in self.children:
                c.prepare()
            self.src = """
            window.setTimeout(
                (function(){
                    %s
                }), %i);""" % (
                    ';\n'.join(c.src for c in self.children),
                    self.exec_delay)
        super(CompoundJSSource, self).prepare()

