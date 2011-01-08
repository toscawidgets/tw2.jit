"""
This file contains baseclasses for thejit widgets
 - JitWidget - contains parameters common to all jit widgets
 - JitTreeOrGraphWidget - contains parameters common to Tree and Graph Widgets
"""

import tw2.core as twc
from tw2.core.resources import JSLink, CSSLink
from tw2.core.resources import JSSymbol, JSFuncCall
from tw2.core.resources import JSSource
from tw2.core.widgets import WidgetMeta
from tw2.core.widgets import Widget

from tw2.jit import jit_base
from tw2.jit.resources import CompoundJSSource
            
import tw2.jquery

from string import Formatter

# TODO -- the tw2 devtools give me __name__ as tw2.jit.widgets but the resources are all in tw2.jit/static
modname = ".".join(__name__.split('.')[:-1])
modname = "tw2.jit"

# TODO -- what's the right way to choose minified or not in tw2?
jit_yc_js = JSLink(modname=modname, filename="%s/jit-yc.js" % jit_base)
jit_js = JSLink(modname=modname, filename="%s/jit.js" % jit_base)
jit_glue_js = JSLink(modname=modname, filename="static/js/tw2.jit.glue.js")
jit_css = CSSLink(modname=modname, filename="static/css/jit_base.css")

# TODO -- redo all of these with mako so we have examples of that and genshi
class JitWidget(twc.Widget):
    """ Baseclass for all other tw2.jit.widgets
    
    Provides a set of parameters common to widgets in the library.

    Uses tw2.jit.resources.CompoundJSSource for client-side initialization
    """

    template = "tw2.jit.templates.jitwidget"
    resources = [jit_js, jit_glue_js]
   
    # Internal twc Variables
    jitClassName = twc.Variable('Name of the Jit class for this widget')
    jitSecondaryClassName = twc.Variable(
        'Secondary Jit class for this widget', default=None)

    injectInto = twc.Variable(
        'name of the DOM element containing the canvas',
        attribute=True, default=property(lambda s: s.compound_id))
    config = twc.Variable( 'jsonified version of other attrs.', default={} )
    # End internal twc Variables

    # Start twc Params
    init_delay = twc.Param(
        'value in milliseconds to delay js initialization and rendering',
        default=0)

    postInitJSCallback = twc.Param(
        'javascript to run after client-side initialization of the widget',
        default=JSSymbol(src='(function(jitwidget){})'), attribute=True)
    
    data = twc.Param('python data to be jsonified and passed to the widget',
                    default=None, attribute=True)
    url = twc.Param('url to json data to be loaded into the widget',
                   default=None, attribute=True)
    # End twc Params

    # Start twc Attributes
    backgroundcolor = twc.Param(
        '(string) background color of the jit container div',
        default='#3a3a3a', attribute=True)

    width = twc.Param('(string) widget width', default='750',attribute=True)

    height = twc.Param('(string) widget height', default='750',attribute=True)
    
    animate = twc.Param(
        '(boolean) Whether to add animated transitions.',
        default=True, attribute=True)
    
    duration = twc.Param(
        '(number) Duration of the animation in milliseconds.',
        default=1000, attribute=True)

    fps = twc.Param(
        '(number) Frames per second of the animation.',
        default=45, attribute=True)
    
    offset = twc.Param(
        '(number) Margin between the display and the canvas.',
        default=25, attribute=True)

    Canvas = twc.Param(
        '(dict) Of the form Options.Canvas in the jit docs.', attribute=True,
        default = {
            'width' : False,
            'height' : False,
            'useCanvas' : False,
            'withLabels' : True,
            'background' : False
        })

    Label = twc.Param(
        '(dict) Of the form Options.Label in the jit docs.', attribute=True,
        default={
            'overridable' : False,
            'type': 'HTML',
            'style' : ' ',
            'size': 10,  
            'family': 'sans-serif',
            'textAlign' : 'center',
            'textBaseline' : 'alphabetic',
            'color': 'white',
        })
    Tips = twc.Param(
        '(dict) Of the form of Options.Tips in the jit docs.', attribute=True,
        default={
            'enable' : False,  
            'type' : 'auto',  
            'offsetX' : 20,  
            'offsetY' : 20,  
            'onShow' : "(function() {})",
            'onHide' : "(function() {})",
        })
    Events = twc.Param(
        '(dict) Of the form Options.Events in the jit docs.', attribute=True,
        default={
            'enable': False,  
            'type': 'auto',  
            'onClick': '(function() {})',  
            'onRightClick': '(function() {})',  
            'onMouseMove': '(function() {})',  
            'onMouseEnter': '(function() {})',  
            'onMouseLeave': '(function() {})',  
            'onDragStart': '(function() {})',  
            'onDragMove': '(function() {})',  
            'onDragCancel': '(function() {})',  
            'onDragEnd': '(function() {})',  
            'onTouchStart': '(function() {})',  
            'onTouchMove': '(function() {})',  
            'onTouchEnd': '(function() {})',  
            'onTouchCancel': '(function() {})',  
            'onMouseWheel': '(function() {})' 
        })

    jsVariables = twc.Param(
        'A dictionary of special jsVariables for substitution',
        default={
            '$$url': lambda s: s.url,
            '$$jitwidget': lambda s:'window._jitwidgets["%s"]' % s.compound_id,
        }
    )
    # End twc attrs


    @classmethod
    def request(cls, req):
        msg = "Subclass of %s must override 'request' for ajax." % cls.__name__
        raise UnimplementedError, msg

    def prepare(self):
        super(JitWidget, self).prepare()

        # Some validation
        if not self.jitClassName:
            msg = "{0.__name__} requires a 'jitClassName'.".format(type(self))
            raise ValueError, msg

        if not self.data and not self.url:
            msg = "%s requires 'data' or 'url' param." % self.__class__.__name__
            raise ValueError, msg

        for k, v in self.attrs.iteritems():
            if type(v) in [JSSymbol]:
                for var, fun in jsVariables.iteritems():
                    res = fun(self)
                    if res:
                        self.attrs[k].src = v.src.replace(var, res)

        setupcall = JSFuncCall(
            function='var jitwidget = setupTW2JitWidget',
            args=[
                self.jitClassName,
                self.jitSecondaryClassName,
                self.compound_id,
                self.attrs
            ])
        if self.data:
            # For normal loading
            loadcall = JSFuncCall(
                function='jitwidget.loadJSON',
                args=[self.data],)
            postcall = JSSource(src=self.postInitJSCallback.src+'(jitwidget)')
        else:
            # For asynchronous loading
            self.resources.append(tw2.jquery.jquery_js)
            loadcall = None
            postcall = JSSource(src="""
                                $.getJSON(
                                    '%s',
                                    function (data) {
                                        // load data when we get it
                                        jitwidget.loadJSON(data);
                                        // Do post-init stuff
                                        %s(jitwidget);
                                    }
                               );""" % (self.url, self.postInitJSCallback.src))

        composite_js_call = CompoundJSSource(
            exec_delay=self.init_delay,
            setupcall=setupcall,
            loadcall=loadcall,
            postcall=postcall)

        self.resources.append(composite_js_call)

    
class JitTreeOrGraphWidget(JitWidget):
    """ Baseclass common to all Tree and Graph JitWidgets """

    # TODO - http://thejit.org/static/v20/Docs/files/Options/Options-Controller-js.html#Options.Controller
    Navigation = twc.Param(
        '(dict) Panning and zooming options for Graph/Tree visualziations.',
        default={
            'enable': False,
            'type': 'auto',
            'panning': False, #True, 'avoid nodes'  
            'zooming': False
        }, attribute=True)
 
    Node = twc.Param(
        '(dict) Provides Node rendering options for ' +
        'Tree and Graph based visualizations.',
        default = {
    #        'overridable': False,  
    #        'type': 'circle',  
            'color': '#ccb',  
            'alpha': 1,  
            'dim': 3,  
            'height': 20,  
            'width': 90,  
            'autoHeight': False,  
            'autoWidth': False,  
            'lineWidth': 1,  
            'transform': True,  
            'align': "center",  
            'angularWidth':1,  
            'span':1,  
            'CanvasStyles': {}  
        }, attribute=True)

    Edge = twc.Param(
        "(dict) Provides Edge rendering options for " +
        "Tree and Graph based visualizations.",
        default = {
    #        'overridable': False,
    #        'type': 'line',  
            'color': '#ccb',  
            'lineWidth': 1,  
            'dim':15,  
            'alpha': 1,  
            'CanvasStyles': {} 
        }, attribute=True)

    onBeforeCompute = twc.Param(
        "(javascript) This method is called right before performing all " +
        "computations and animations.  The selected Graph.Node " +
        "is passed as parameter.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onAfterCompute = twc.Param(
        "(javascript) This method is triggered after all animations " +
        "or computations ended.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onCreateLabel = twc.Param(
        "(javascript) This method receives a new label DIV element as " +
        "first parameter, and the corresponding Graph.Node  as second " +
        "parameter.  This method will only be called once for each label.  " +
        "This method is useful when adding events or styles to the labels " +
        "used by the JIT.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onPlaceLabel = twc.Param(
        "(javascript) This method receives a label DIV element as first " +
        "parameter and the corresponding Graph.Node  as second parameter.  " +
        "This method is called each time a label has been placed in the " +
        "visualization, for example at each step of an animation, and thus " +
        "it allows you to update the labels properties, such as size or " +
        "position.  Note that onPlaceLabel will be triggered after updating " +
        "the labels positions.  That means that, for example, the left and " +
        "top css properties are already updated to match the nodes " +
        "positions.  Width and height properties are not set however.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onBeforePlotNode = twc.Param(
        "(javascript) This method is triggered right before plotting " +
        "each Graph.Node.  This method is useful for changing a node " +
        "style right before plotting it.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onAfterPlotNode = twc.Param(
        "(javascript) This method is triggered right after plotting " +
        "each Graph.Node.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onBeforePlotLine = twc.Param(
        "(javascript) This method is triggered right before plotting " +
        "a Graph.Adjacence.  This method is useful for adding some " +
        "styles to a particular edge before being plotted.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    onAfterPlotLine = twc.Param(
        "(javascript) This method is triggered right after plotting " +
        "a Graph.Adjacence.",
        default=JSSymbol(src="(function(node) {})"), attribute=True)
