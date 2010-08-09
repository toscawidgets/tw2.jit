import tw2.core as twc
from tw2.core.resources import JSLink, CSSLink
from tw2.core.resources import JSSource
from tw2.jit import jit_base
from simplejson.encoder import JSONEncoder

# TODO -- is this line going to get run over and over?  singleton?
encoder = JSONEncoder() 

# TODO -- the tw2 devtools are give me __name__ as tw2.jit.widgets but the resources are all in tw2.jit/static
modname = ".".join(__name__.split('.')[:-1])
modname = "tw2.jit"

# TODO -- what's the right way to choose minified or not in tw2
jit_yc_js = JSLink(modname=modname, filename="%s/jit-yc.js" % jit_base)
jit_js = JSLink(modname=modname, filename="%s/jit.js" % jit_base)
jit_css = CSSLink(modname=modname, filename="static/css/jit_base.css")
treemap_css = CSSLink(modname=modname, filename="static/css/treemap.css")
sunburst_css = CSSLink(modname=modname, filename="static/css/sunburst.css")
icicle_css = CSSLink(modname=modname, filename="static/css/icicle.css")

# TODO -- redo all of these with mako so we have examples of that and genshi
class JitWidget(twc.Widget):
    preinitJS = twc.Param(
        'javascript to run before init of the widget', default='')
    postinitJS = twc.Param(
        'javascript to run after init of the widget', default='')
    
    jitClassName = twc.Variable('Name of the Jit class for this widget')

    injectInto = twc.Variable(
        description='name of the DOM element containing the canvas',
        attribute=True, default=property(lambda s: s.compound_id))

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

    #Label = twc.Param(
    #    '(dict) Of the form Options.Label in the jit docs.', attribute=True,
    #    default={
    #        'overridable' : False,
    #        'type': 'Native',
    #        'style' : ' ',
    #        'size': 10,  
    #        'family': 'sans-serif',
    #        'textAlign' : 'center',
    #        'textBaseline' : 'alphabetic',
    #        'color': 'white',
    #    })
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

    registered_javascript_attrs = {}

    def prepare(self):
        super(JitWidget, self).prepare()
        self.config = encoder.encode(self.attrs)
        self.json = encoder.encode(self.data)
        self.registered_javascript_attrs = encoder.encode(
            self.registered_javascript_attrs)
    

