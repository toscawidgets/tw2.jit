import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js

class JitGraph(JitTreeOrGraphWidget):
    """ Baseclass for graph widgets """
    pass

class RadialGraph(JitGraph):
    """ A radial graph visualization with advanced animations.

    See thejit API documentation on RadialGraph:
        http://thejit.org/static/v20/Docs/files/Visualizations/RGraph-js.html
    """

    jitClassName = 'RGraph'

    background = twc.Param(
        '(dict) see sample.', default={},
        attribute=True, request_local=False)
   
class ForceDirectedGraph(JitGraph):
    """ A visualization that lays graphs using a Force-Directed layout algorithm.

    See thejit API documentation on ForceDirectedGraph:
        http://thejit.org/static/v20/Docs/files/Visualizations/ForceDirected-js.html
    """

    jitClassName = 'ForceDirected'
    
    iterations = twc.Param(
        '(number) The number of iterations for the spring ' +
        'layout simulation.  Depending on the browser\'s ' +
        'speed you could set this to a more "interesting" ' +
        'number, like 200.',
        default=2, attribute=True, request_local=False)
    
    levelDistance = twc.Param(
        '(number) The natural length desired for the edges.',
        default=50, attribute=True, request_local=False)

class AsynchronousRadialGraph(RadialGraph):
    """ * Work in progress and not yet fit for use * """

    preprocessTree = twc.Param(attribute=True, default=JSSymbol(src="""
    (function(json) {
      var ch = json.children;
      var getNode = function(nodeName) {
        for(var i=0; i<ch.length; i++) {
          if(ch[i].name == nodeName) return ch[i];
        }
        return false;
      };
      var rgraph = $$jitwidget;
      json.id = rgraph.root;
      console.log('JSON id is:' + json.id);
      $jit.Graph.Util.eachAdjacency(rgraph.graph.getNode(rgraph.root),
          function(elem) {
            var nodeTo = elem.nodeTo, jsonNode = getNode(nodeTo.name);
            if(jsonNode) jsonNode.id = nodeTo.id;
          });
    })"""))

    requestGraph = twc.Param(attribute=True, default=JSSymbol(src="""
       (function() {
        var that = this, id = this.clickedNodeId;
        console.log("requesting info <em>please wait...</em>");
        $.getJSON(
            '$$url' + encodeURIComponent(that.clickedNodeName) + '/',
            function(json) {
            console.log("morphing...");
            that.preprocessTree(json);
            var op = $jit.ST.Op($$jitwidget.viz);
            $jit.Graph.Op.viz = $$jitwidget;
            $jit.Graph.Op.morph($$jitwidget, json, {
                'id': id,
                'type': 'fade',
                'duration':2000,
                hideLabels:true,
                onAfterCompute: (function() {} ),
                onBeforeCompute: (function() {}),
          });
        });
    })"""))
    
    onAfterCompute = JSSymbol(src=" (function() { this.requestGraph(); })")

    postInitJSCallback = JSSymbol(src="""
    (function(jitwidget) {
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
        console.log('setting up json call');
        $.getJSON(
           '$$url' + name + '/',
            function(json) {
          //load weighted graph.
         jitwidget.loadJSON(json);
          //compute positions
          jitwidget.compute();
          console.log("done");
          jitwidget.controller.clickedNodeName = name;
        });
    })""")

