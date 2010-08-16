import tw2.core as twc
from tw2.core.resources import JSSource

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js

from tw2.jit.defaults import ForceDirectedGraphJSONDefaults

# TODO -- PANIC -- what should thsi include from JitChart??? or JitTree?
class JitGraph(JitTreeOrGraphWidget):
    pass

#Radial Graph
class RadialGraph(JitGraph):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(default='RGraph')

    background = twc.Param(
        '(dict) see sample (TODO).', default={},
        attribute=True, request_local=False)
   
class ForceDirectedGraph(JitGraph):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(default='ForceDirected')
    
    data = twc.Param(default=ForceDirectedGraphJSONDefaults)
    postinitJS = twc.Param(default="""
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
            'onShow' : JSSource(src="""
            (function(tip, node) {
                var count = 0;
                node.eachAdjacency(function() { count++; });
                tip.innerHTML = '<div class="tip-title">' 
                    + node.name + '</div>'
                    + '<div class="tip-text"><b>connections:</b> ' 
                    + count + '</div>';
                  })
            """)
        }, attribute=True, request_local=False)
    Events = twc.Param(
        '(dict) As per usual.',
        default={
            'enable' : True,
            'onMouseEnter' : JSSource(src="""
            (function() { 
                jitwidget.canvas.getElement().style.cursor = \'move\';
            })"""),
            'onMouseLeave' : JSSource(src="""
            (function() {
                jitwidget.canvas.getElement().style.cursor = \'\';
            })"""),
            'onDragMove' : JSSource(src="""
            (function(node, eventInfo, e) {
                var pos = eventInfo.getPos();
                node.pos.setc(pos.x, pos.y);
                jitwidget.plot();
            })"""),
            'onTouchMove' : JSSource(src="""
            (function(node, eventInfo, e) {
                $jit.util.event.stop(e);
                this.onDragMove(node, eventInfo, e);
            })"""),
            'onClick' : JSSource(src="""
            (function(node) {
                if(!node) return;
                var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
                list = [];
                node.eachAdjacency(function(adj){
                    list.push(adj.nodeTo.name);
                });
                alert("this is connected to: " + list.join(", "));
            })""")
        }, attribute=True, request_local=False)

    onCreateLabel = twc.Param(
        '(string) Javascript callback bizniz',
        default=JSSource(src="""
        (function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.fontSize = "0.8em";
              style.color = "#ddd";
        })"""), attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
        '(string) Javascript callback bizzzzniz',
        default=JSSource(src="""
        (function(domElement, node){
            var style = domElement.style;
            var left = parseInt(style.left);
            var top = parseInt(style.top);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
            style.top = (top + 10) + 'px';
            style.display = '';
        })"""), attribute=True, request_local=False)

    iterations = twc.Param(
        '(number) The number of iterations for the spring ' +
        'layout simulation.  Depending on the browser\'s ' +
        'speed you could set this to a more "interesting" ' +
        'number, like 200.',
        default=2, attribute=True, request_local=False)
    
    levelDistance = twc.Param(
        '(number) The natural length desired for the edges.',
        default=50, attribute=True, request_local=False)

