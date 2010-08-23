
from tw2.core.resources import JSSymbol

from tw2.jit.widgets import AreaChart
from tw2.jit.widgets import BarChart
from tw2.jit.widgets import PieChart
from tw2.jit.widgets import RadialGraph

from tw2.jit.defaults import AreaChartJSONDefaults
from tw2.jit.defaults import BarChartJSONDefaults
from tw2.jit.defaults import PieChartJSONDefaults
from tw2.jit.defaults import RadialGraphJSONDefaults

class DemoAreaChart(AreaChart):
    data = AreaChartJSONDefaults

class DemoBarChart(BarChart):
    data = BarChartJSONDefaults

class DemoPieChart(PieChart):
    data = PieChartJSONDefaults
    sliceOffset = 5 


from tw2.jit.widgets import RadialGraph
from tw2.jit.defaults import RadialGraphJSONDefaults

class DemoRadialGraph(RadialGraph):
    data = RadialGraphJSONDefaults

    background = { 'CanvasStyles':{ 'strokeStyle' : '#555' } }

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
                jitwidget.onClick(node.id);
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
from tw2.jit.defaults import ForceDirectedGraphJSONDefaults

class DemoForceDirectedGraph(ForceDirectedGraph):
    data = ForceDirectedGraphJSONDefaults

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
                jitwidget.canvas.getElement().style.cursor = \'move\';
            })"""),
            'onMouseLeave' : JSSymbol(src="""
            (function() {
                jitwidget.canvas.getElement().style.cursor = \'\';
            })"""),
            'onDragMove' : JSSymbol(src="""
            (function(node, eventInfo, e) {
                var pos = eventInfo.getPos();
                node.pos.setc(pos.x, pos.y);
                jitwidget.plot();
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

from tw2.jit.widgets import TreeMap
from tw2.jit.defaults import TreeMapJSONDefaults
class DemoTreeMap(TreeMap):
    data = TreeMapJSONDefaults

    postInitJSCallback = JSSymbol(
        src="(function (jitwidget) { jitwidget.refresh(); })")

    Tips = {
        'enable' : True,
        'offsetX' : 20,
        'offsetY' : 20,
        'onShow' : JSSymbol(src="""
            (function(tip, node, isLeaf, domElement) {
                   var html = '<div class="tip-title">' + node.name   
                     + '</div><div class="tip-text">';  
                   var data = node.data;  
                   if(data.playcount) {  
                     html += 'play count: ' + data.playcount;  
                   }  
                   if(data.image) {  
                        html += '<img src="'+ data.image +'" style="width: 100px; margin: 3px;" />';  
                   }  
                   tip.innerHTML =  html;   
            })
            """)
    }

    onCreateLabel = JSSymbol(src="""
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
        """)
    

from tw2.jit.widgets import Sunburst
from tw2.jit.defaults import SunburstJSONDefaults
class DemoSunburst(Sunburst):
    data = SunburstJSONDefaults
    
    postInitJSCallback = JSSymbol(
        src="(function (jitwidget) { jitwidget.refresh(); })")

    #Node = {
    #    'overridable' : True,
    #    'type' : 'gradient-multiple',
    #}

    Label = { 'type' : 'HTML' }
    NodeStyles = {
            'enable': True,
            'type': 'HTML',
            'stylesClick': {
                'color': '#33dddd'
            },
            'stylesHover': {
                'color': '#dd3333'
            }
    }

    #onCreateLabel = JSSymbol(src="""
    #(function(domElement, node){
    #   var labels = jitwidget.config.Label.type;
    #   var aw = node.getData('angularWidth');  
    #   if (labels === 'HTML' && (node._depth < 2 || aw > 2000)) {  
    #     domElement.innerHTML = node.name;  
    #   } else if (labels === 'SVG' && (node._depth < 2 || aw > 2000)) {  
    #     domElement.firstChild.appendChild(document.createTextNode(node.name));  
    #   }  
    # })""")
    onPlaceLabel = JSSymbol(src="""
        (function(domElement, node){  
            var labels = jitwidget.config.Label.type;  
            if (labels === 'SVG') {  
                var fch = domElement.firstChild;  
                var style = fch.style;  
                style.display = '';  
                style.cursor = 'pointer';  
                style.fontSize = '0.8em';  
                fch.setAttribute('fill', '#fff');  
            } else if (labels === 'HTML') {  
                var style = domElement.style;  
                style.display = '';  
                style.cursor = 'pointer';  
                style.fontSize = '0.8em';  
                style.color = '#ddd';  
                var left = parseInt(style.left);  
                var w = domElement.offsetWidth;  
                style.left = (left - w / 2) + 'px';  
            }  
        })""")

    Tips = {
        'enable': True,  
        'onShow': JSSymbol(src="""
            (function(tip, node) {  
                var html = '<div class="tip-title">' + node.name + '</div>';
                var data = node.data;  
                if('days' in data) {  
                    html += '<b>Last modified:</b> ' + data.days + ' days ago';
                }  
                if('size' in data) {  
                    html += '<br /><b>File size:</b> ' + Math.round(data.size / 1024) + 'KB';
                }
                tip.innerHTML = html;  
            })""")
    }
    Events = {
        'enable': True,
        'onClick': JSSymbol(src="""
            (function(node) {  
                if(!node) return;  
                jitwidget.tips.hide();  
                jitwidget.rotate(node, 'animate', {  
                    duration: 1000,  
                    transition: $jit.Trans.Quart.easeInOut  
                });  
            })""")
    }



from tw2.jit.widgets import HyperTree
from tw2.jit.defaults import HyperTreeJSONDefaults
class DemoHyperTree(HyperTree):
    data = HyperTreeJSONDefaults
    
    postInitJSCallback = JSSymbol(
        src="(function (jitwidget) { jitwidget.refresh(); })")

    Node = {
        'dim' : 9,
        'color' : '#f00',
    }

    Edge = {
        'lineWidth' : 2,
        'color' : '#088',
    }
    
    onCreateLabel = JSSymbol(src="""
            ( function(domElement, node){
                  domElement.innerHTML = node.name;
                  $jit.util.addEvent(domElement, 'click', function () {
                      jitwidget.onClick(node.id);
                  });
            })""")

    onPlaceLabel = JSSymbol(src="""
            ( function(domElement, node){
                  var style = domElement.style;
                  style.display = '';
                  style.cursor = 'pointer';
                  if (node._depth <= 1) {
                      style.fontSize = '0.8em';
                      style.color = '#ddd';
                  } else if(node._depth == 2){
                      style.fontSize = '0.7em';
                      style.color = '#555';
                  } else {
                      style.display = 'none';
                  }
                  var left = parseInt(style.left);
                  var w = domElement.offsetWidth;
                  style.left = (left - w / 2) + 'px';
              })""")


from tw2.jit.widgets import SpaceTree
from tw2.jit.defaults import SpaceTreeJSONDefaults
class DemoSpaceTree(SpaceTree):
    data = SpaceTreeJSONDefaults
    
    postInitJSCallback = JSSymbol(
        src="""
        (function (jitwidget) {
            jitwidget.compute();
            jitwidget.geom.translate(
                new $jit.Complex(-200, 0), "current");
            jitwidget.onClick(jitwidget.root);
            jitwidget.refresh(); 
    })""")

    Navigation = {
        'enable' : True,
        'panning' : True,
    }
    Node = {
        'overridable' : True,
        'height' : 20,
        'width' : 60,
        'type' : 'rectangle',
        'color' : '#aaa',
    }
            
    Edge = {
        'type' : 'bezier',
        'overridable' : True
    }

    onCreateLabel = JSSymbol(src="""
        (function(label, node){
            label.id = node.id;            
            label.innerHTML = node.name;
            label.onclick = function(){
                jitwidget.onClick(node.id);
            };
            var style = label.style;
            style.width = 60 + 'px';
            style.height = 17 + 'px';            
            style.cursor = 'pointer';
            style.color = '#333';
            style.fontSize = '0.8em';
            style.textAlign= 'center';
            style.paddingTop = '3px';
        })""")

    onBeforePlotNode = JSSymbol(src="""
        (function(node){
            if (node.selected) {
                node.data.$color = \'#ff7\';
            }
            else {
                delete node.data.$color;
                if(!node.anySubnode(\'exist\')) {
                    var count = 0;
                    node.eachSubnode(function(n) { count++; });
                    node.data.$color = [
                                '#aaa', '#baa', '#caa', 
                                '#daa', '#eaa', '#faa'][count];                    
                }
            }
        })""")
    onBeforePlotLine = JSSymbol(src="""
        (function(adj){
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
                adj.data.$color = \'#eed\';
                adj.data.$lineWidth = 3;
            }
            else {
                delete adj.data.$color;
                delete adj.data.$lineWidth;
            }
        })""")

from tw2.jit.widgets import Icicle 
from tw2.jit.defaults import IcicleJSONDefaults
class DemoIcicle(Icicle):
    data = IcicleJSONDefaults
    
    postInitJSCallback = JSSymbol(
        src="(function (jitwidget) { jitwidget.refresh(); })")

    Tips = {
        'enable': True,  
        'type' : 'HTML',
        'offsetX' : 20,
        'offsetY' : 20,
        'onShow': JSSymbol(src="""
            (function(tip, node){
                var count = 0;
                node.eachSubnode(function(){
                  count++;
                }); // TODO -- working here.. quotes are broke.
                tip.innerHTML = '<div class="tip-title"><b>Name:</b> ' 
                    + node.name + '</div><div class=\\'tip-text\\'>' 
                    + count + ' children</div>';
            })"""),
    }

    Events = {
        'enable': True,
        'onMouseEnter': JSSymbol(src="""
            (function(node) {
                node.setData('border', '#33dddd');
                jitwidget.fx.plotNode(node, jitwidget.canvas);
                jitwidget.labels.plotLabel(
                                 jitwidget.canvas,
                                 node,
                                 jitwidget.controller);
            })"""),
        'onMouseLeave': JSSymbol(src="""
            (function(node) {
                node.removeData('border');
                jitwidget.fx.plot();
            })"""),
        'onClick': JSSymbol(src="""
            (function(node){
                if (node) {
                    jitwidget.tips.hide();
                    if(jitwidget.events.hoveredNode){
                        this.onMouseLeave(jitwidget.events.hoveredNode);
                    }
                    jitwidget.enter(node);
               }
            })"""),
        'onRightClick': JSSymbol(src="""
            (function(){
                jitwidget.tips.hide();
                if(jitwidget.events.hoveredNode) {
                    this.onMouseLeave(jitwidget.events.hoveredNode);
                }
                jitwidget.out();
            })"""),
    }
    onCreateLabel = JSSymbol(src="""
         (function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.fontSize = '0.9em';
              style.display = '';
              style.cursor = 'pointer';
              style.color = '#CCC';
              style.overflow = 'hidden';
        })""")
    onPlaceLabel = JSSymbol(src="""
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
        })""")


