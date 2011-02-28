""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import AjaxRadialGraph
from tw2.jit.samples_data import RadialGraphJSONSampleData

import commands

def make_node(package, prefix):
    return {
        'id': prefix + "___" + package,
        'name': package,
        'children': [],
        'data': []
    }

def get_dependency_tree(package, n=1, prefix=''):
    package = package.strip()
    print "Working on", package
    out = commands.getoutput(
        "yum deplist %s | grep dependency | awk ' { print $2 } '" % package)
    out = list(set([dep.split('(')[0] for dep in out.split('\n') if dep]))

    root = make_node(package, prefix)
    prefix = "%s_%s" % (prefix, package)

    if n > 0:
        [root['children'].append(
            get_dependency_tree(dep, n-1, prefix)) for dep in out]
    else:
        [root['children'].append(make_node(dep, prefix)) for dep in out]
    return root


class DemoAjaxRadialGraph(AjaxRadialGraph):
    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        if 'id' not in req.params:
            id = 'wine'
        else:
            id = req.params['id'].split('___')[-1]
        json = get_dependency_tree(id)
        return json

    url = '/db_radialgraph_demo/'

    def prepare(self):
        super(DemoAjaxRadialGraph, self).prepare()
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
              jitwidget.compute();
              jitwidget.plot();
              $('#wine').click();
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
            var ch = json.children;
            var getNode = function(nodeName) {
                for(var i=0; i<ch.length; i++) {
                    if(ch[i].name == nodeName) return ch[i];
                }
                return false;
            };
            json.id = jitwidget.root;
            $jit.Graph.Util.eachAdjacency(
                jitwidget.graph.getNode(jitwidget.root),
                function(elem) {
                    var nodeTo = elem.nodeTo, jsonNode = getNode(nodeTo.name);
                    if(jsonNode) {  jsonNode.id = nodeTo.id; }
                }
            );
        })""")
    requestGraph = JSSymbol(src="""
        (function() {
            var that = this, id = this.clickedNodeId;
            var jsonRequest = $.ajax({
                url: '%s?id=' + encodeURIComponent(id),
                dataType: 'json',
                success:  function (json) {
                    that.preprocessTree(json);
                    jitwidget.op.morph(json, {
                        id: id,
                        type: 'fade',
                        duration:2000,
                        transition: $jit.Trans.Quart.easeOut,
                        hideLabels:true,
                        onAfterCompute: (function(){}),
                        onBeforeCompute: (function(){}),
                    });

                    var old = jitwidget.graph.getNode(jitwidget.oldRootToRemove);
                    if ( !old ) return;
                    var subnodes = old.getSubnodes(0);
                    var map = [];
                    for ( var i = 0; i < subnodes.length; i++ ) {
                        map.push(subnodes[i].id);
                    }
                    map.push(jitwidget.oldRootToRemove);

                    jitwidget.op.removeNode(map.reverse(), {
                        type: 'fade:seq',
                        duration: 2000,
                        onAfterCompute: (function(){}),
                        onBeforeCompute: (function(){}),
                    });
                },
            });
        })""")

    onBeforeCompute = JSSymbol(src="""
        (function (node) {
            jitwidget.oldRootToRemove = node.getParents()[0].id;
            this.clickedNodeId = node.id;
         })""")

    onAfterCompute = JSSymbol(src="(function() { this.requestGraph(); })")

    onCreateLabel = JSSymbol(src="""
        (function(domElement, node) {
            $(domElement).html(node.name);
            $(domElement).click(function() {
                jitwidget.onClick(domElement.id);
            });
        })""")

    onPlaceLabel = JSSymbol(src="""
        (function(domElement, node){
            domElement.style.display = "none";
            domElement.innerHTML = node.name;
            domElement.style.display = "";
            var left = parseInt(domElement.style.left);
            domElement.style.width = '';
            domElement.style.height = '';
            var w = domElement.offsetWidth;
            domElement.style.left = (left - w /2) + 'px';

            // This should all be moved to a css file
            domElement.style.backgroundcolor = '#222';
            domElement.style.cursor = 'pointer';
            if ( node._depth <= 1 )
                domElement.style.color = 'white';
            else
                domElement.style.color = 'grey';
        })""")

import tw2.core as twc
mw = twc.core.request_local()['middleware']
mw.controllers.register(DemoAjaxRadialGraph, 'db_radialgraph_demo')
