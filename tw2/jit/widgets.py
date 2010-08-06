import tw2.core as twc, re, itertools, webob, cgi
from tw2.core.resources import JSLink, CSSLink
from tw2.core.resources import JSSource
from tw2.jit import jit_base
from simplejson.encoder import JSONEncoder

from tw2.jit.defaults import AreaChartJSONDefaults
from tw2.jit.defaults import BarChartJSONDefaults
from tw2.jit.defaults import PieChartJSONDefaults
from tw2.jit.defaults import TreeMapJSONDefaults
from tw2.jit.defaults import ForceDirectedGraphJSONDefaults
from tw2.jit.defaults import RadialGraphJSONDefaults
from tw2.jit.defaults import SunburstJSONDefaults
from tw2.jit.defaults import IcicleJSONDefaults
from tw2.jit.defaults import SpaceTreeJSONDefaults
from tw2.jit.defaults import HyperTreeJSONDefaults

encoder = JSONEncoder() 

jit_yc_js = JSLink(modname=__name__, filename="%s/jit-yc.js" % jit_base)
jit_js = JSLink(modname=__name__, filename="%s/jit.js" % jit_base)
jit_css = CSSLink(modname=__name__, filename="static/css/jit_base.css")
treemap_css = CSSLink(modname=__name__, filename="static/css/treemap.css")
sunburst_css = CSSLink(modname=__name__, filename="static/css/sunburst.css")
icicle_css = CSSLink(modname=__name__, filename="static/css/icicle.css")

class JitWidget(twc.Widget):
    # TODO -- what's the right way to choose minified or not?
    #resources = [jit_yc_js]
    resources = [jit_js]

    preinitJS = twc.Param(
        'javascript to run before initialization of the jit widget',
        default='', request_local=False, attribute=True)
    postinitJS = twc.Param(
        'javascript to run after initialization of the jit widget',
        default='', request_local=False, attribute=True)

    injectInto = twc.Variable(
        description='dom name',
        request_local=False,
        attribute=True,
        default=property(lambda s: s.compound_id))
    width = twc.Param(
        description='(string) width of the widget',
        request_local=False,
        attribute=True,
        default='500')
    height = twc.Param(
        description='(string) height of the widget',
        request_local=False,
        attribute=True,
        default='500')
    Canvas = twc.Param(
        '(dict) Of the form Options.Canvas in the jit docs.',
        default = {
            'width' : False,
            'height' : False,
            'useCanvas' : False,
            'withLabels' : True,
            'background' : False
        }, attribute=True, request_local=False)
    Label = twc.Param(
        '(dict) Of the form Options.Label in the jit docs.',
        default={
            'overridable' : False,
            'type': 'HTML',
            'style' : ' ',
            'size': 10,  
            'family': 'sans-serif',
            'textAlign' : 'center',
            'textBaseline' : 'alphabetic',
            'color': 'black',
        }, attribute=True, request_local=False)
    Tips = twc.Param(
        '(dict) Of the form of Options.Tips in the jit docs.',
        default={
            'enable' : False,  
            'type' : 'auto',  
            'offsetX' : 20,  
            'offsetY' : 20,  
            'onShow' : "(function() {})",
            'onHide' : "(function() {})",
        }, attribute=True, request_local=False)
    Events = twc.Param(
        '(dict) Of the form Options.Events in the jit docs.',
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
        }, attribute=True, request_local=False)
    animate = twc.Param(
        '(boolean) Whether to add animated transitions ' +
        'when filtering/restoring stacks',
        default=True, attribute=True, request_local=False)
    config = twc.Variable( 'jsonified version of other attrs.', default={} )
    json = ''

    registered_javascript_attrs = {}

    def prepare(self):
        super(JitWidget, self).prepare()
        self.config = encoder.encode(self.attrs)
        self.json = encoder.encode(self.json)
        self.registered_javascript_attrs = encoder.encode(
            self.registered_javascript_attrs)


class JitChart(JitWidget):
    offset = twc.Param(
        '(number) Adds margin between the visualiziation ' + 
        'and the canvas.',
        default=25, attribute=True, request_local=False)
    type = twc.Param(
        '(string) Stack style.  Possible values are ' + 
        '"stacked", "stacked:gradient" to add gradients.',
        default='stacked', attribute=True, request_local=False)
    showLabels = twc.Param(
        '(boolean) Display the name of the slots.',
        default=True, attribute=True, request_local=False)
    labelOffset = twc.Param(
        '(number) Adds margin between the label and the ' +
        'default place where it should be drawn.',
        default=3, attribute=True, request_local=False)

class AreaChart(JitChart):
    # TODO -- redo this with mako to have an example of either
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='AreaChart')

    selectOnHover = twc.Param(
        '(boolean) If true, it will add a mark to the ' +
        'hovered stack.',
        default=True, attribute=True, request_local=False)
    showAggregates = twc.Param(
        '(boolean) Display the sum of the values of the ' +
        'different stacks.',
        default=True, attribute=True, request_local=False)
    filterOnClick = twc.Param(
        '(boolean) Select the clicked stack by hiding ' +
        'all other stacks.',
        default=True, attribute=True, request_local=False)
    restoreOnRightClick = twc.Param(
        '(boolean) Show all stacks by right clicking.',
        default=True, attribute=True, request_local=False)

    Label = twc.Param(
        'dictionary of parameters for the labels',
        default={
            'type' : 'Native',
            'size' : 20,
            'family' : 'Arial',
            'color' : 'white'
        }, attribute=True, request_local=False)

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=AreaChartJSONDefaults, attribute=True, request_local=False)

class BarChart(JitChart):
    # TODO -- redo this with mako to have an example of either
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='BarChart')
    
    barsOffset = twc.Param(
        '(number) Separation between bars.',
        default=0, attribute=True, request_local=False)
    hoveredColor = twc.Param(
        '(string) Sets the selected color for a hovered bar stack.',
        default='#9fd4ff', attribute=True, request_local=False)
    orientation = twc.Param(
        '(string) Sets the direction of the bars.  Possible ' +
        'options are "vertical" and "horizontal".',
        default='horizontal', attribute=True, request_local=False)
    showAggregates = twc.Param(
        '(boolean) Display the sum of the values of the ' +
        'different stacks.',
        default=True, attribute=True, request_local=False)

    Label = twc.Param(
        'dictionary of parameters for the labels',
        default={
            'type' : 'Native',
            'size' : 20,
            'family' : 'Arial',
            'color' : 'white'
        }, attribute=True, request_local=False)

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=BarChartJSONDefaults, attribute=True, request_local=False)

class PieChart(JitChart):
    # TODO -- redo this with mako to have an example of either
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='PieChart')

    sliceOffset = twc.Param(
        '(number) Separation between the center of the ' +
        'canvas and each pie slice.',
        default=0, attribute=True, request_local=False)
    hoveredColor = twc.Param(
        '(string) Sets the selected color for a hovered pie stack.',
        default='#9fd4ff', attribute=True, request_local=False)
    resizeLabels = twc.Param(
        '(boolean|number) Resize the pie labels according to ' +
        'their stacked values.  Set a number for resizeLabels ' +
        'to set a font size minimum.',
        default=False, attribute=True, request_local=False)
    updateHeights = twc.Param(
        '(boolean) Only for mono-valued (most common) pie ' +
        'charts.  Resize the height of the pie slices ' +
        'according to their current values.',
        default=False, attribute=True, request_local=False)
    
    Label = twc.Param(
        'dictionary of parameters for the labels',
        default={
            'type' : 'Native',
            'size' : 20,
            'family' : 'Arial',
            'color' : 'white'
        }, attribute=True, request_local=False)

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=PieChartJSONDefaults, attribute=True, request_local=False)

class JitTree(JitChart):
    constrained = twc.Param(
        '(boolean) Whether to show the entire tree when loaded ' +
        'or just the number of levels specified by levelsToShow.',
        default=False, attribute=True, request_local=False)
    levelsToShow = twc.Param(
        '(number) The number of levels to show for a subtree.  This ' +
        'number is relative to the selected node.',
        default=3, attribute=True, request_local=False)
    duration = twc.Param(
        '(number) Duration of the animation in milliseconds.',
        default=700, attribute=True, request_local=False)
    fps = twc.Param(
        '(number) Frames per second of the animation.',
        default=45, attribute=True, request_local=False)

class TreeMap(JitTree):
    resources = [jit_js, jit_css, treemap_css]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='TM.Squarified')
    
    postinitJS = twc.Param(
        'whatevs',
        default="jitwidget.refresh();", attribute=True, request_local=False)
   
    registered_javascript_attrs = {
        'Events' : {
            'onClick' : True,
            'onRightClick' : True,
        },
        'Tips' : {
            'onShow' : True,
        },
        'onCreateLabel' : True
    }
    
    Events = twc.Param(
        '(dict) Of the form Options.Events in the jit docs.',
        default={
            'enable': True,
            'onClick': '(function(node) {if (node) { jitwidget.enter(node); }})',
            'onRightClick': '(function() {jitwidget.out();})',
        }, attribute=True, request_local=False)
    Tips = twc.Param(
        '(dict) Of the form of Options.Tips in the jit docs.',
        default={
            'enable' : True,
            'offsetX' : 20,  
            'offsetY' : 20,  
            'onShow' :
            """
            (function(tip, node, isLeaf, domElement) {
                   var html = '<div class=\"tip-title\">' + node.name   
                     + '</div><div class=\"tip-text\">';  
                   var data = node.data;  
                   if(data.playcount) {  
                     html += 'play count: ' + data.playcount;  
                   }  
                   if(data.image) {  
            html += '<img src=\"'+ data.image +'\" style=\"width: 100px; margin: 3px;\" />';  
                   }  
                   tip.innerHTML =  html;   
                 })
            """,
        }, attribute=True, request_local=False)
    onCreateLabel = twc.Param(
        '(string) Javascript callback definition.',
        default="""
        (function(domElement, node){  
           domElement.innerHTML = node.name;  
           var style = domElement.style;  
           style.display = '';  
           style.border = '1px solid transparent';  
           domElement.onmouseover = function() {  
             style.border = '1px solid #9FD4FF';  
           };  
           domElement.onmouseout = function() {  
             style.border = '1px solid transparent';  
           };  
        } )
        """, attribute=True, request_local=False)
    orientation = twc.Param(
        '(string) Whether to set horizontal or vertical layout.  ' +
        'Possible values are "h" or "v".',
        default='h', attribute=True, request_local=False)
    titleHeight = twc.Param(
        '(number) Separation between the center of the ' +
        'canvas and each pie slice.',
        default=13, attribute=True, request_local=False)
    offset = twc.Param(
        '(number) Boxes offset.',
        default=2, attribute=True, request_local=False)
    # TODO - Node.Type 
    #see http://thejit.org/static/v20/Docs/files/Visualizations/Treemap-js.html
    #duration and fps too
    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=TreeMapJSONDefaults, attribute=True, request_local=False)

class JitGraph(JitChart):
    pass

class ForceDirectedGraph(JitGraph):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='ForceDirected')
    
    postinitJS = twc.Param(
        'whatevs',
        default="""
  // compute positions incrementally and animate.
  jitwidget.computeIncremental({
    iter: 40,
    property: 'end',
    onComplete: function(){
      jitwidget.animate({
        modes: ['linear'],
        transition: $jit.Trans.Elastic.easeOut,
        duration: 2500
      });
    }
  });""", attribute=True, request_local=False)

    Navigation = twc.Param(
        '(dict) As per Options.Navigation.',
        default={
            'enable' : True,
            'panning' : 'avoid nodes',
            'zooming' : 10
        }, attribute=True, request_local=False)
    Node = twc.Param(
        '(dict) As per Options.Node.',
        default={
            'overridable' : True,
        }, attribute=True, request_local=False)
    Edge = twc.Param(
        '(dict) As per Options.Edge.',
        default={
            'overridable' : True,
            'color' : '#23A4FF',
            'lineWidth' : 0.4,
        }, attribute=True, request_local=False)
    Label = twc.Param(
        '(dict) As per Options.Label.',
        default={
            'style' : 'bold',
        }, attribute=True, request_local=False)
    Tips = twc.Param(
        '(dict) As per Options.Tips.',
        default={
            'enable' : True,
            'onShow' : """
            (function(tip, node) {
                //count connections
                var count = 0;
                node.eachAdjacency(function() { count++; });
                //display node info in tooltip
                tip.innerHTML = '<div class=\"tip-title\">' 
                    + node.name + '</div>'
                    + '<div class=\"tip-text\"><b>connections:</b> ' 
                    + count + '</div>';
                  })
            """
        }, attribute=True, request_local=False)
    Events = twc.Param(
        '(dict) As per usual.',
        default={
            'enable' : True,
            'onMouseEnter' : """
            (function() { 
                jitwidget.canvas.getElement().style.cursor = \'move\';
            })""",
            'onMouseLeave' : """
            (function() {
                jitwidget.canvas.getElement().style.cursor = \'\';
            })""",
            'onDragMove' : """
            (function(node, eventInfo, e) {
                var pos = eventInfo.getPos();
                node.pos.setc(pos.x, pos.y);
                jitwidget.plot();
            })""",
            'onTouchMove' : """
            (function(node, eventInfo, e) {
                $jit.util.event.stop(e); //stop default touchmove event
                this.onDragMove(node, eventInfo, e);
            })""",
            'onClick' : """
            (function(node) {
                if(!node) return;
                // Build the right column relations list.
                // This is done by traversing the clicked node connections.
                var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
                list = [];
                node.eachAdjacency(function(adj){
                    list.push(adj.nodeTo.name);
                });
                alert("this is connected to: " + list.join(", "));
            })"""
        }, attribute=True, request_local=False)

    onCreateLabel = twc.Param(
        '(string) Javascript callback bizniz',
        default="""
        (function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.fontSize = "0.8em";
              style.color = "#ddd";
        })""", attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
        '(string) Javascript callback bizzzzniz',
        default="""
        (function(domElement, node){
            var style = domElement.style;
            var left = parseInt(style.left);
            var top = parseInt(style.top);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
            style.top = (top + 10) + 'px';
            style.display = '';
        })""", attribute=True, request_local=False)

    registered_javascript_attrs = {
        'onCreateLabel' : True,
        'onPlaceLabel' : True,
        'Events' : {
            'onMouseEnter' : True,
            'onMouseLeave' : True,
            'onDragMove' : True,
            'onTouchMove' : True,
            'onClick' : True,
        },
        'Tips' : {
            'onShow' : True,
        },
    }

    iterations = twc.Param(
        '(number) The number of iterations for the spring ' +
        'layout simulation.  Depending on the browser\'s ' +
        'speed you could set this to a more "interesting" ' +
        'number, like 200.',
        default=2, attribute=True, request_local=False)
    
    levelDistance = twc.Param(
        '(number) The natural length desired for the edges.',
        default=50, attribute=True, request_local=False)
    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=ForceDirectedGraphJSONDefaults,
        attribute=True, request_local=False)

#Radial Graph
class RadialGraph(JitGraph):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='RGraph')
    
    postinitJS = twc.Param(
        'whatevs',
        default="""
    //trigger small animation for kicks
    jitwidget.graph.eachNode(function(n) {
        var pos = n.getPos();
        pos.setc(-200, -200);
    });
    jitwidget.compute('end');
    jitwidget.fx.animate({
        modes:['polar'],
        duration: 2000
    });""", attribute=True, request_local=False)
   
    background = twc.Param(
        '(dict) see ... TODO.',
        default={
            'CanvasStyles':{
                'strokeStyle' : '#555'
            }
        }, attribute=True, request_local=False)
    Node = twc.Param(
        '(dict) .. blah.',
        default={
            'color': '#ddeeff',
        }, attribute=True, request_local=False)
    Edge = twc.Param(
        '(dict) .. blah.',
        default={
            'color': '#C17878',
            'lineWidth':1.5,
        }, attribute=True, request_local=False)
    onCreateLabel = twc.Param(
        'javascript function callback',
        default="""
        (function(domElement, node){
            domElement.innerHTML = node.name;
            domElement.onclick = function(){
                jitwidget.onClick(node.id);
            };
        })""", attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
        'javascript function callback',
        default="""
        (function(domElement, node){
            var style = domElement.style;
            style.display = '';
            style.cursor = 'pointer';

            if (node._depth <= 1) {
                style.fontSize = "0.8em";
                style.color = "#ccc";
            
            } else if(node._depth == 2){
                style.fontSize = "0.7em";
                style.color = "#494949";
            
            } else {
                style.display = 'none';
            }

            var left = parseInt(style.left);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
        })""", attribute=True, request_local=False)
    
    registered_javascript_attrs = {
        'onCreateLabel' : True,
        'onPlaceLabel' : True,
    }

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=RadialGraphJSONDefaults,
        attribute=True, request_local=False)

    
class Sunburst(JitWidget):
    resources = [jit_js, sunburst_css, jit_css]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='Sunburst')

    postinitJS = twc.Param(
        'whatevs',
        default="jitwidget.refresh();", attribute=True, request_local=False)

    levelDistance = twc.Param(
        '(number) Distance between levels.',
        default=90, attribute=True, request_local=False)
    Node = twc.Param(
        '(dict)',
        default = {
            'overridable' : True,
            'type' : 'gradient-multipie',
        }, attribute=True, request_local=False)
    Label = twc.Param(
        '(dict)',
        default = {
            'type' : 'HTML',
        }, attribute=True, request_local=False)
    NodeStyles = twc.Param(
        '(dict)',
        default={
            'enable': True,  
            'type': 'HTML',  
            'stylesClick': {  
                'color': '#33dddd'  
            },  
            'stylesHover': {  
                'color': '#dd3333'  
            }  
        }, attribute=True, request_local=False)
    Tips = twc.Param(
        '(dict)',
        default={
            'enable': True,  
            'onShow': """
            (function(tip, node) {  
                var html = '<div class=\"tip-title\">' + node.name + '</div>';
                var data = node.data;  
                if('days' in data) {  
                    html += '<b>Last modified:</b> ' + data.days + ' days ago';
                }  
                if('size' in data) {  
                    html += '<br /><b>File size:</b> ' + Math.round(data.size / 1024) + 'KB';
                }
                tip.innerHTML = html;  
            })"""}, attribute=True, request_local=False)
    Events = twc.Param(
        default= {
            'enable': True,
            'onClick': """
        (function(node) {  
         if(!node) return;  
         //hide tip  
         jitwidget.tips.hide();  
         //rotate  
         jitwidget.rotate(node, 'animate', {  
           duration: 1000,  
           transition: $jit.Trans.Quart.easeInOut  
         });  
       })"""}, attribute=True, request_local=False)
    onCreateLabel = twc.Param(
         '(string) javascript callback.',
         default="""
         (function(domElement, node){
       var labels = jitwidget.config.Label.type,  
           aw = node.getData('angularWidth');  
       if (labels === 'HTML' && (node._depth < 2 || aw > 2000)) {  
         domElement.innerHTML = node.name;  
       } else if (labels === 'SVG' && (node._depth < 2 || aw > 2000)) {  
         domElement.firstChild.appendChild(document.createTextNode(node.name));  
       }  
     })""",
         attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
         '(string) javascript callback.',
         default="""
     (function(domElement, node){  
       var labels = jitwidget.config.Label.type;  
       if (labels === 'SVG') {  
         var fch = domElement.firstChild;  
         var style = fch.style;  
         style.display = '';  
         style.cursor = 'pointer';  
         style.fontSize = "0.8em";  
         fch.setAttribute('fill', "#fff");  
       } else if (labels === 'HTML') {  
         var style = domElement.style;  
         style.display = '';  
         style.cursor = 'pointer';  
         style.fontSize = "0.8em";  
         style.color = "#ddd";  
         var left = parseInt(style.left);  
         var w = domElement.offsetWidth;  
         style.left = (left - w / 2) + 'px';  
       }  
     })""", attribute=True, request_local=False)
   
    registered_javascript_attrs = {
        'Tips' : { 'onShow' : True },
        'Events' : { 'onClick' : True },
        'onPlaceLabel' : True,
        'onCreateLabel' : True,
    }

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=SunburstJSONDefaults,
        attribute=True, request_local=False)

class JitTree(JitWidget):
    animate = twc.Param(
        '(boolean)', default=True, attribute=True, request_local=False)

    offset = twc.Param(
        '(number)', default=1, attribute=True, request_local=False)

    cushion = twc.Param(
        '(boolean)', default=1, attribute=True, request_local=False)

    constrained = twc.Param(
        '(boolean)', default=True, attribute=True, request_local=False)
    levelsToShow = twc.Param(
        '(number)', default=3, attribute=True, request_local=False)

class HyperTree(JitTree):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.hypertree"
    w = twc.Variable( 'width of the canvas.', default=500 )
    h = twc.Variable( 'height of the canvas.', default=500 )
    
    offset = twc.Param(
        '(number)', default=0, attribute=True, request_local=False)

    def prepare(self):
        super(HyperTree, self).prepare()
        self.w = self.width
        self.h = self.height
    
    registered_javascript_attrs = {
        'onPlaceLabel' : True,
        'onCreateLabel' : True,
    }
   
    postinitJS = twc.Param(
        'whatevs',
        default="jitwidget.refresh();", attribute=True, request_local=False)

    Node = twc.Param(
        '(dict)',
        default = {
            'dim' : 9,
            'color' : '#f00',
        }, attribute=True, request_local=False)
    Edge = twc.Param(
        '(dict)',
        default = {
            'lineWidth' : 2,
            'color' : '#088',
        }, attribute=True, request_local=False)
    onCreateLabel = twc.Param(
         '(string) javascript callback.',
         default="""
            ( function(domElement, node){
                  domElement.innerHTML = node.name;
                  $jit.util.addEvent(domElement, 'click', function () {
                      jitwidget.onClick(node.id);
                  });
            })""", attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
        '(string) javascript callback.',
        default="""
            ( function(domElement, node){
                  var style = domElement.style;
                  style.display = '';
                  style.cursor = 'pointer';
                  if (node._depth <= 1) {
                      style.fontSize = "0.8em";
                      style.color = "#ddd";

                  } else if(node._depth == 2){
                      style.fontSize = "0.7em";
                      style.color = "#555";

                  } else {
                      style.display = 'none';
                  }

                  var left = parseInt(style.left);
                  var w = domElement.offsetWidth;
                  style.left = (left - w / 2) + 'px';
              })""", attribute=True, request_local=False)

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=HyperTreeJSONDefaults,
        attribute=True, request_local=False)



class SpaceTree(JitTree):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='ST')
    
    postinitJS = twc.Param(
        'whatever',
        default="jitwidget.compute();jitwidget.geom.translate(new $jit.Complex(-200, 0), \"current\");jitwidget.onClick(jitwidget.root);", attribute=True, request_local=False)

    duration = twc.Param(
        'foo',
        default=800, attribute=True, request_local=False)
    transition = twc.Param(
        'javascript',
        default='$jit.Trans.Quart.easeInOut', attribute=True, request_local=False)
    levelDistance = twc.Param(
        'foo',
        default=50, attribute=True, request_local=False)

    Navigation = twc.Param(
        'alsdkfjalsdjkfalskfj',
        default={
            'enable' : True,
            'panning' : True,
        }, attribute=True, request_local=False)

    Node = twc.Param(
        '(dict)',
        default = {
            'height' : 20,
            'width' : 60,
            'type' : 'rectangle',
            'color' : '#aaa',
            'overridable' : True
        }, attribute=True, request_local=False)

    Edge = twc.Param(
        '(dict)',
        default = {
            'type' : 'bezier',
            'overridable' : True
        }, attribute=True, request_local=False)

    onCreateLabel = twc.Param(
        'dofalsdkjfadf',
        default="""
        (function(label, node){
            label.id = node.id;            
            label.innerHTML = node.name;
            label.onclick = function(){
                jitwidget.onClick(node.id);
            };
            //set label styles
            var style = label.style;
            style.width = 60 + 'px';
            style.height = 17 + 'px';            
            style.cursor = 'pointer';
            style.color = '#333';
            style.fontSize = '0.8em';
            style.textAlign= 'center';
            style.paddingTop = '3px';
        })""", attribute=True, request_local=False)
    onBeforePlotNode = twc.Param(
        'asdlfkjasdlkfj',
        default="""
        (function(node){
            //add some color to the nodes in the path between the
            //root node and the selected node.
            if (node.selected) {
                node.data.$color = "#ff7";
            }
            else {
                delete node.data.$color;
                //if the node belongs to the last plotted level
                if(!node.anySubnode("exist")) {
                    //count children number
                    var count = 0;
                    node.eachSubnode(function(n) { count++; });
                    //assign a node color based on
                    //how many children it has
                    node.data.$color = ['#aaa', '#baa', '#caa', '#daa', '#eaa', '#faa'][count];                    
                }
            }
        })""", attribute=True, request_local=False)
    onBeforePlotLine = twc.Param(
        'asdlkfjasldfjka',
        default="""
        (function(adj){
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
                adj.data.$color = "#eed";
                adj.data.$lineWidth = 3;
            }
            else {
                delete adj.data.$color;
                delete adj.data.$lineWidth;
            }
        })""", attribute=True, request_local=False)

    registered_javascript_attrs = {
        'transition' : True,
        'onCreateLabel' : True,
        'onBeforePlotLine' : True,
        'onBeforePlotNode' : True,
    }

    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=SpaceTreeJSONDefaults,
        attribute=True, request_local=False)

class Icicle(JitTree):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(
        'name of the Jit class for this widget', default='Icicle')
    
    postinitJS = twc.Param(
        'whatevs',
        default="jitwidget.refresh();", attribute=True, request_local=False)
    
    json = twc.Param(
        '(dict) Data to send to the widget.',
        default=IcicleJSONDefaults,
        attribute=True, request_local=False)

    Tips = twc.Param(
        '(dict)',
        default={
            'enable': True,  
            'type' : 'Native',
            'offsetX' : 20,
            'offsetY' : 20,
            'onShow': """
            (function(tip, node){
                // count children
                var count = 0;
                node.eachSubnode(function(){
                  count++;
                });
                // add tooltip info
                tip.innerHTML = '<div class=\"tip-title\"><b>Name:</b> ' 
                    + node.name + '</div><div class=\"tip-text\">' 
                    + count + ' children</div>';
            })"""}, attribute=True, request_local=False)
    Events = twc.Param(
        default= {
            'enable': True,
            'onMouseEnter': """
            (function(node) {
                //add border and replot node
                node.setData('border', '#33dddd');
                jitwidget.fx.plotNode(node, jitwidget.canvas);
                jitwidget.labels.plotLabel(jitwidget.canvas, node, jitwidget.controller);
            })""",
            'onMouseLeave': """
            (function(node) {
                node.removeData('border');
                jitwidget.fx.plot();
            })""",
            'onClick': """
            (function(node){
                if (node) {
                    //hide tips and selections
                    jitwidget.tips.hide();
                    if(jitwidget.events.hoveredNode)
                        this.onMouseLeave(jitwidget.events.hoveredNode);
                    //perform the enter animation
                    jitwidget.enter(node);
               }
            })""",
            'onRightClick': """
            (function(){
                //hide tips and selections
                jitwidget.tips.hide();
                if(jitwidget.events.hoveredNode)
                    this.onMouseLeave(jitwidget.events.hoveredNode);
                //perform the out animation
                jitwidget.out();
            })""",
      }, attribute=True, request_local=False)
    onCreateLabel = twc.Param(
         '(string) javascript callback.',
         default="""
         (function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.fontSize = '0.9em';
              style.display = '';
              style.cursor = 'pointer';
              style.color = '#333';
              style.overflow = 'hidden';
        })""", attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
         '(string) javascript callback.',
         default="""
            (function(domElement, node){
                  var style = domElement.style,
                      width = node.getData('width'),
                      height = node.getData('height');
                  if(width < 7 || height < 7) {
                    style.display = 'none';
                  } else {
                    style.display = '';
                    style.width = width + 'px';
                    style.height = height + 'px';
                  }
        })""", attribute=True, request_local=False)
    registered_javascript_attrs = {
        'Tips' : { 'onShow' : True },
        'Events' : {
            'onMouseEnter' : True,
            'onMouseLeave' : True,
            'onClick' : True,
            'onRightClick' : True
        },
        'onCreateLabel' : True,
        'onPlaceLabel' : True,
    }
    pass

