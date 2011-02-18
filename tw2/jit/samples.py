""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import DbRadialGraph
from tw2.jit.samples_data import RadialGraphJSONSampleData


class DemoDbRadialGraph(DbRadialGraph):
    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):

        def subtree_of(id, graph):
            print id, "versus", graph['id']
            if unicode(graph['id']) == id:
                return graph

            for subtree in graph.get('children', []):
                result = subtree_of(id, subtree)
                if result:
                    # Found it!
                    import copy
                    # This is so ugly ;; works for now
                    parent = copy.deepcopy(graph)
                    del parent['children']
                    result['children'].append(parent)
                    return result

            return {}

        if 'id' not in req.params or req.params['id'] == 'undefined':
            result = RadialGraphJSONSampleData
        else:
            result = subtree_of(req.params['id'], RadialGraphJSONSampleData)
        if not result:
            print "NO SUBTREE FOUND AT ALL"
        def tighten_up_children(graph):
            if not 'children' in graph:
                graph['children'] = []

            for i in range(len(graph['children'])):
                graph['children'][i] = tighten_up_children(graph['children'][i])

            return graph

        result = tighten_up_children(result)

        def prune_result(graph):
            import copy
            newgraph = copy.deepcopy(graph)
            for i in range(len(newgraph['children'])):
                del newgraph['children'][i]['children']
            return newgraph

        result = prune_result(result) 
        return result

    url = '/db_radialgraph_demo/'

    def prepare(self):
        super(DemoDbRadialGraph, self).prepare()
        # Used for doing ajax stuff
        import tw2.jquery
        self.resources.append(tw2.jquery.jquery_js)

        # Add the ajax url to the request graph source
        if '%s' in self.requestGraph.src:
            self.requestGraph.src = self.requestGraph.src % self.url

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

    preprocessTree = JSSymbol(src="""
        (function(json) {
                              console.log('innnit');
            var ch = json.children;
            var getNode = function(nodeName) {
                for(var i=0; i<ch.length; i++) {
                    if(ch[i].name == nodeName) return ch[i];
                }
                return false;
            };
                              console.log(json.id);
            json.id = jitwidget.root;
                              console.log(json.id);
                              console.log("whadddup");
            $jit.Graph.Util.eachAdjacency(
                jitwidget.graph.getNode(jitwidget.root),
                function(elem) {
                    var nodeTo = elem.nodeTo, jsonNode = getNode(nodeTo.name);
                    if(jsonNode) {
                        console.log(jsonNode.id + "  " + nodeTo.id);
                        jsonNode.id = nodeTo.id;
                    }
                }
            );
                                console.log("outties");
        })""")
    requestGraph = JSSymbol(src="""
        (function() {
                            console.log('request graph in');
            var that = this, id = this.clickedNodeId;
            var jsonRequest = $.ajax({
                url: '%s?id=' + encodeURIComponent(id),
                dataType: 'json',
                success:  function (json) {
                    that.preprocessTree(json);
                    jitwidget.op.morph(json, {
                        'id': id,
                        'type': 'fade',
                        'duration':2000,
                        hideLabels:true,
                        onAfterCompute: (function(){}),
                        onBeforeCompute: (function(){}),
                    });
                },
            });
                            console.log('request graph out');
        })""")

    onBeforeCompute = JSSymbol(src="""
        (function (node) {
           // TODO -- track history here.
           this.clickedNodeId = node.id;
         })""")

    onAfterCompute = JSSymbol(src="(function() { this.requestGraph(); })")

    onCreateLabel = JSSymbol(src="""
        (function(domElement, node) {
            console.log("create label...");
                             console.log(domElement);
                             console.log(domElement.id);
            $(domElement).html(node.name);
            $(domElement).click(function() {jitwidget.onClick(domElement.id);});
        })""")

    onPlaceLabel = JSSymbol(src="""
        (function(domElement, node){
            domElement.style.display = "none";
            if(node._depth <= 1) {
                domElement.innerHTML = node.name;
                domElement.style.display = "";
                var left = parseInt(domElement.style.left);
                domElement.style.width = '';
                domElement.style.height = '';
                var w = domElement.offsetWidth;
                domElement.style.left = (left - w /2) + 'px';

                // This should all be moved to a css file
                domElement.style.color = 'white';
                domElement.style.backgroundcolor = '#222';
                domElement.style.cursor = 'pointer;'
            }
        })""")

import tw2.core as twc
mw = twc.core.request_local()['middleware']
mw.controllers.register(DemoDbRadialGraph, 'db_radialgraph_demo')
