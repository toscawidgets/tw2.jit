""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import RadialGraph
from tw2.jit.samples.samples_data import RadialGraphJSONSampleData
class DemoRadialGraph(RadialGraph):
    data = RadialGraphJSONSampleData

    background = { 'CanvasStyles':{ 'strokeStyle' : '#555' } }
    
    backgroundcolor = '#0f0f0f'

    postInitJSCallback = JSSymbol(src="""
        (function (jitwidget) {
            //trigger small animation for kicks
            jitwidget.graph.eachNode(function(n) {
                var pos = n.getPos();
                pos.setc(-200, -200);
            });
            jitwidget.compute('end');
            jitwidget.fx.animate({
                modes:['polar'],
                duration: 2000
            });
         })""")
    
    Node = {
        'color' : '#ddeeff',
    }
            
    Edge = {
        'color': '#C17878',
        'lineWidth':1.5,
    }

    onCreateLabel = JSSymbol(src="""
        (function(domElement, node){
            domElement.innerHTML = node.name;
            domElement.onclick = function(){
                $$jitwidget.onClick(node.id);
            };
        })""")
    onPlaceLabel = JSSymbol(src="""
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
        })""")


from tw2.jit.widgets import ForceDirectedGraph
from tw2.jit.samples.samples_data import ForceDirectedGraphJSONSampleData
class DemoForceDirectedGraph(ForceDirectedGraph):
    data = ForceDirectedGraphJSONSampleData

    iterations = 25

    levelDistance = 75

    postInitJSCallback = JSSymbol(src=""" 
        (function (jitwidget) {
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
            });
        })""")

    Navigation = {
        'enable' : True,
        'panning' : 'avoid nodes',
        'zooming' : 10
    }
    Node = {
        'overridable' : True,
    }
    Edge = {
        'overridable' : True,
        'color' : '#23A4FF',
        'lineWidth' : 0.4,
    }
    Label = {
        'style' : 'bold',
    }
    Tips = {
        'enable' : True,
        'onShow' : JSSymbol(src="""
            (function(tip, node) {
                var count = 0;
                node.eachAdjacency(function() { count++; });
                tip.innerHTML = '<div class="tip-title">' 
                    + node.name + '</div>'
                    + '<div class="tip-text"><b>connections:</b> ' 
                    + count + '</div>';
            })"""),
    }

    Events = {
            'enable' : True,
            'onMouseEnter' : JSSymbol(src="""
            (function() { 
                $$jitwidget.canvas.getElement().style.cursor = \'move\';
            })"""),
            'onMouseLeave' : JSSymbol(src="""
            (function() {
                $$jitwidget.canvas.getElement().style.cursor = \'\';
            })"""),
            'onDragMove' : JSSymbol(src="""
            (function(node, eventInfo, e) {
                var pos = eventInfo.getPos();
                node.pos.setc(pos.x, pos.y);
                $$jitwidget.plot();
            })"""),
            'onTouchMove' : JSSymbol(src="""
            (function(node, eventInfo, e) {
                $jit.util.event.stop(e);
                this.onDragMove(node, eventInfo, e);
            })"""),
            'onClick' : JSSymbol(src="""
            (function(node) {
                if(!node) return;
                var html = "<h4>" + node.name + "</h4><b> connections:</b><ul><li>",
                list = [];
                node.eachAdjacency(function(adj){
                    list.push(adj.nodeTo.name);
                });
                alert("this is connected to: " + list.join(", "));
            })""")
    }
    onCreateLabel = JSSymbol(src="""
        (function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.fontSize = "0.8em";
              style.color = "#ddd";
        })""" )
    onPlaceLabel = JSSymbol(src="""
        (function(domElement, node){
            var style = domElement.style;
            var left = parseInt(style.left);
            var top = parseInt(style.top);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
            style.top = (top + 10) + 'px';
            style.display = '';
        })""")
