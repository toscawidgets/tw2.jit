import tw2.core as twc
from tw2.core.resources import JSLink, CSSLink
from tw2.core.resources import JSSymbol, JSFuncCall
from tw2.core.resources import JSSource
from tw2.core.resources import encoder
from tw2.core.widgets import WidgetMeta
from tw2.core.widgets import Widget

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

# TODO -- redo all of these with mako so we have examples of that and genshi
class JitWidget(twc.Widget):
    resources = [jit_js, jit_glue_js]

    postInitJSCallback = twc.Param(
        'javascript to run after client-side initialization of the widget',
        default=JSSymbol(src='(function(jitwidget){})'))
    
    jitClassName = twc.Variable('Name of the Jit class for this widget')
    jitSecondaryClassName = twc.Variable(
        'Secondary Jit class for this widget', default=None)

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

        # TODO -- can this class be made more generic?
        # I crapped it out based on specific needs to make multiple
        #   calls that would share the same jitwidget js variable in
        #   the same scope, but not conflict with other JitWidget's js space.
        class CompositeJSFuncCall(JSSource):
            """
            Two inline javascript function calls and a jssource
            """
            func1 = twc.Param('Function 1 name')
            args1 = twc.Param('Function 1 args')
            func2 = twc.Param('Function 2 name')
            args2 = twc.Param('Function 2 args')
            ext_src = twc.Param('Third Inline javascript')
            src = None
            location = 'bodybottom'
        
            def prepare(self):
                if not self.src:
                    if isinstance(self.args1, dict):
                        args1 = encoder.encode(self.args)
                    elif self.args1:
                        args1 = ', '.join(encoder.encode(a) for a in self.args1)
                    self.src1 = '%s(%s)' % (self.func1, args1)
                    if isinstance(self.args2, dict):
                        args2 = encoder.encode(self.args)
                    elif self.args2:
                        args2 = ', '.join(encoder.encode(a) for a in self.args2)
                    self.src2 = '%s(%s)' % (self.func2, args2)
                    self.src = "(function(){\n%s;\n%s;\n%s\n})();" % \
                            (self.src1, self.src2, self.ext_src)
                super(CompositeJSFuncCall, self).prepare()

        # Use the above defined class
        composite_js_call = CompositeJSFuncCall(
            func1='var jitwidget = setupTW2JitWidget',
            args1=[
                self.jitClassName,
                self.jitSecondaryClassName,
                self.attrs
            ],
            func2='jitwidget.loadJSON',
            args2=[self.data],
            ext_src=self.postInitJSCallback.src+"(jitwidget);"
        )
        self.resources.append(composite_js_call)


    
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
        "Provides Edge rendering options for " +
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
