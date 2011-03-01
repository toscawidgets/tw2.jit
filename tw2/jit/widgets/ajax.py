import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js
from tw2.jit.widgets.graph import RadialGraph

# Used for doing ajax stuff
import tw2.jquery

class AjaxRadialGraph(RadialGraph):
    """ A radial graph that pulls nodes on demand.

    WARNING : the "Live Demo" sample is hosted on a very slow machine.
    When you click, be very patient.

    Based off of the following demo:
        http://demos.thejit.org/lpkgd/#

    See thejit API documentation on RadialGraph for more information:
        http://thejit.org/static/v20/Docs/files/Visualizations/RGraph-js.html

    """

    def prepare(self):
        super(AjaxRadialGraph, self).prepare()
        self.resources.append(tw2.jquery.jquery_js)

        # Add the ajax url to the request graph source
        if '%s' in self.attrs['requestGraph'].src:
            self.attrs['requestGraph'] = JSSymbol(src=self.requestGraph.src % self.url)

    url = twc.Param(""" TODO """)

    preprocessTree = twc.Param(
        """ TODO """, attribute=True,
        default=JSSymbol(src="""
        (function(json) {
            json.id = jitwidget.root;
        })"""))

    requestGraph = twc.Param(
        """ TODO """, attribute=True,
        default=JSSymbol(src="""
        (function() {
            var that = this, id = this.clickedNodeId;
            var jsonRequest = $.ajax({
                url: '%s?key=' + encodeURIComponent(id),
                dataType: 'json',
                success:  function (json) {
                    that.preprocessTree(json);
                    jitwidget.op.morph(json, {
                        id: id,
                        type: 'fade',
                        duration:100,
                        transition: $jit.Trans.Quart.easeOut,
                        hideLabels:true,
                        onAfterCompute: (function(){}),
                        onBeforeCompute: (function(){}),
                    });

                    function hasID(json, id) {
                         if ( json.id == id ) return true;

                         for ( var i = 0; i < json.children.length; i++ ) {
                            if ( hasID(json.children[i], id) ) return true;
                         }
                         return false;
                    }

                    var old = jitwidget.graph.getNode(jitwidget.root);
                    if ( !old ) return;
                    var subnodes = old.getSubnodes(1);
                    var map = [];
                    for ( var i = 0; i < subnodes.length; i++ ) {
                        if ( ! hasID(json, subnodes[i].id) ) {
                            map.push(subnodes[i].id);
                        }
                    }

                    jitwidget.op.removeNode(map.reverse(), {
                        type: 'fade:seq',
                        duration: 100,
                        onAfterCompute: (function(){}),
                        onBeforeCompute: (function(){}),
                    });
                },
            });
        })"""))

    onBeforeCompute = JSSymbol(src="""
        (function (node) {
            jitwidget.oldRootToRemove = node.getParents()[0].id;
            this.clickedNodeId = node.id;
         })""")

    onAfterCompute = JSSymbol(src="(function() { this.requestGraph(); })")

    onCreateLabel = JSSymbol(src="""
        (function(domElement, node) {
            try {
                jQuery(domElement).html(node.name);
                jQuery(domElement).click(function() {
                    jitwidget.onClick(domElement.id);
                    // TODO -- figure out something to really do with data here.
                    // Here's one example:
                    //if ( node.data.url ) window.location = node.data.url;
                });
            } catch(err) {}
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

