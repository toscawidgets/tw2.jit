import tw2.core as twc

from tw2.jit.widgets.core import JitWidget
from tw2.jit.widgets.core import jit_js

from tw2.jit.defaults import ForceDirectedGraphJSONDefaults
from tw2.jit.defaults import RadialGraphJSONDefaults

# TODO -- PANIC -- what should thsi include from JitChart??? or JitTree?
class JitGraph(JitWidget):
    pass

class ForceDirectedGraph(JitGraph):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(default='ForceDirected')
    
    json = twc.Param(default=ForceDirectedGraphJSONDefaults)
    
    postinitJS = twc.Param(default="""
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

#Radial Graph
class RadialGraph(JitGraph):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(default='RGraph')

    json = twc.Param(default=RadialGraphJSONDefaults)

    postinitJS = twc.Param(
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
