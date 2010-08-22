import tw2.core as twc
from tw2.core.resources import JSLink, CSSLink
from tw2.core.resources import JSSymbol, JSFuncCall
from tw2.core.widgets import WidgetMeta

from tw2.jit import jit_base

from simplejson import JSONEncoder

# TODO -- the tw2 devtools are give me __name__ as tw2.jit.widgets but the resources are all in tw2.jit/static
modname = ".".join(__name__.split('.')[:-1])
modname = "tw2.jit"

# TODO -- what's the right way to choose minified or not in tw2
jit_yc_js = JSLink(modname=modname, filename="%s/jit-yc.js" % jit_base)
jit_js = JSLink(modname=modname, filename="%s/jit.js" % jit_base)
jit_glue_js = JSLink(modname=modname, filename="static/js/tw2.jit.glue.js")
jit_css = CSSLink(modname=modname, filename="static/css/jit_base.css")
treemap_css = CSSLink(modname=modname, filename="static/css/treemap.css")
sunburst_css = CSSLink(modname=modname, filename="static/css/sunburst.css")
icicle_css = CSSLink(modname=modname, filename="static/css/icicle.css")

# TODO -- is this line going to get run over and over?  singleton?
encoder = JSONEncoder() 

# TODO -- redo all of these with mako so we have examples of that and genshi
class JitWidget(twc.Widget):
    resources = [jit_js, jit_glue_js]

    preinitJS = twc.Param(
        'javascript to run before init of the widget', default='')
    postinitJS = twc.Param(
        'javascript to run after init of the widget', default='')
    
    jitClassName = twc.Variable('Name of the Jit class for this widget')

    injectInto = twc.Variable(
        description='name of the DOM element containing the canvas',
        attribute=True, default=property(lambda s: s.compound_id))

    backgroundcolor = twc.Param(
        description='(string) background color of the jit container div',
        default='#1a1a1a', attribute=True)

    width = twc.Param(
        description='(string) widget width', attribute=True, default='500')

    height = twc.Param(
        description='(string) widget height', attribute=True, default='500')
    
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

    config = twc.Variable( 'jsonified version of other attrs.', default={} )



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

    data = twc.Param('python data to be jsonified and passed to the widget')

    def prepare(self):
        super(JitWidget, self).prepare()
        self.resources.append(JSFuncCall(
            parent=self.__class__,
            function='var jitwidget = setupTW2JitWidget',
            args=[JSSymbol(src='jitwidget'), self.jitClassName, self.attrs, self.data]))
    
class JitTreeOrGraphWidget(JitWidget):
    # TODO __
    # http://thejit.org/static/v20/Docs/files/Options/Options-Controller-js.html#Options.Controller
    # Trees and graphs have Navigation
    Navigation = twc.Param(
        'Panning and zooming options for Graph/Tree visualziations.',
        default={
            'enable': False,
            'type': 'auto',
            'panning': False, #True, 'avoid nodes'  
            'zooming': False
        }, attribute=True)
 
    Node = twc.Param(
        'Provides Node rendering options for ' +
        'Tree and Graph based visualizations.',
        default = {
            'overridable': False,  
            'type': 'circle',  
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
        "Provides Edge rendering options for " +
        "Tree and Graph based visualizations.",
        default = {
            'overridable': False,
            'type': 'line',  
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
