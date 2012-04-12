import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_css
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
    data = []
    base_url = twc.Param(default=twc.Required)

    def prepare(self):
        super(AjaxRadialGraph, self).prepare()
        self.resources.extend([tw2.jquery.jquery_js, jit_css])

    preprocessTree = twc.Param(
        """ TODO """, attribute=True,
        default=JSSymbol(src="""
        (function(json) {
            json.id = $$jitwidget.root;
        })"""))

    requestGraph = twc.Param(
        """ TODO """, attribute=True,
        default=JSSymbol(src="""
        (function() {
            var that = this, id = $$jitwidget.clickedNodeId;
            var jsonRequest = $.ajax({
                url: '$$base_url?key=' + encodeURIComponent(id),
                dataType: 'json',
                success:  function (json) {
                    that.preprocessTree(json);
                    $$jitwidget.op.morph(json, {
                        id: id,
                        type: 'fade',
                        duration: $$duration,
                        transition: $$transition,
                        hideLabels:true,
                        onBeforeCompute: (function(){}),
                    });

                    function hasID(json, id) {
                         if ( json.id == id ) return true;

                         for ( var i = 0; i < json.children.length; i++ ) {
                            if ( hasID(json.children[i], id) ) return true;
                         }
                         return false;
                    }

                    var old = $$jitwidget.graph.getNode($$jitwidget.root);
                    if ( !old ) return;
                    var subnodes = old.getSubnodes(1);
                    var map = [];
                    for ( var i = 0; i < subnodes.length; i++ ) {
                        if ( ! hasID(json, subnodes[i].id) ) {
                            map.push(subnodes[i].id);
                        }
                    }

                    $$jitwidget.op.removeNode(map.reverse(), {
                        type: 'fade:seq',
                        duration: $$duration,
                        onBeforeCompute: (function(){}),
                    });
                },
            });
        })"""))

    onBeforeCompute = JSSymbol(src="""
        (function (node) {
            $$jitwidget.oldRootToRemove = node.getParents()[0].id;
            $$jitwidget.clickedNodeId = node.id;
            if ( $$jitwidget.deep_linking ) {
                window.location.hash = $$jitwidget.clickedNodeId;
            }
         })""")

    onCreateLabel = JSSymbol(src="""
        (function(domElement, node) {
            try {
                var that = this;
                jQuery(domElement).html(node.name);
                jQuery(domElement).click(function() {
                    $$jitwidget.onClick(domElement.id, {
                        onComplete: function() {
                             that.requestGraph();
                        }
                    });
                });
                if ( node.data.hover_html ) {
                    if ( window._fadeOutTimeouts === undefined ) { window._fadeOutTimeouts = {}; }
                    if ( window._removeTimeouts === undefined ) { window._removeTimeouts = {}; }

                    var TIP_FADE_TIME = 1000;
                    var TIP_WAIT_TIME = 1000;

                    function remove(hover_id, e) {
                        var fadeOutTimeout = setTimeout(function(){
                            window._fadeOutTimeouts[hover_id] = null;
                            jQuery('#'+hover_id).fadeOut(TIP_FADE_TIME);
                            var removeTimeout = setTimeout(function(){
                                window._removeTimeouts[hover_id] = null;
                                jQuery('#'+hover_id).remove();
                            }, TIP_FADE_TIME);
                            window._removeTimeouts[hover_id] = removeTimeout;
                        },TIP_WAIT_TIME);
                        window._fadeOutTimeouts[hover_id] = fadeOutTimeout;
                    }
                    function unremove(hover_id, e) {
                         clearTimeout(window._fadeOutTimeouts[hover_id]);
                         clearTimeout(window._removeTimeouts[hover_id]);
                    }

                    var hover_id = 'ajaxRadialGraph_' + node.id + '_Tip';

                    // TODO -- this needs some fixin'
                    //hover_id = hover_id.replace(/\./g,'_');
                    //hover_id = hover_id.replace(/\//g, '_');
                    //hover_id = hover_id.replace(/\(/g, '_');
                    //hover_id = hover_id.replace(/\)/g, '_');
                    hover_id = hover_id.replace(new RegExp('\\.', 'g'),'_');

                    jQuery(domElement)
                      .mouseover(
                         function (e) {
                            if ( jQuery('#'+hover_id).length == 0 ) {
                                var pos = jQuery(domElement).offset();
                                var width = jQuery(domElement).width();
                                jQuery('body').prepend("<div id='"+hover_id+"' class='radialGraphTip'></div>");
                                var div = jQuery('#'+hover_id);
                                div.css({
                                    "position":"absolute",
                                    "left":(pos.left+width) + "px",
                                    "top":pos.top + "px"
                                });
                                div.hide().fadeIn(TIP_FADE_TIME);
                                div.append(node.data.hover_html);
                                div.mouseover(function(e){unremove(hover_id, e);});
                                div.mouseout(function(e){remove(hover_id, e);});
                            }
                         })
                       .mouseout(
                          function (e) {
                            if ( jQuery('#'+hover_id).length == 0 ) { return; }
                            remove(hover_id, e);
                          });
                }
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
    postInitJSCallback = JSSymbol(
        src="""
        (function (jitwidget) {
              jitwidget.compute();
              jitwidget.plot();
              jitwidget.deep_linking = $$deep_linking;
              if ( jitwidget.deep_linking && window.location.hash != '' ) {
                  jitwidget.clickedNodeId = window.location.hash;
                  $.getJSON(
                    '$$base_url?key='+encodeURIComponent(jitwidget.clickedNodeId),
                    function (data) {
                        jitwidget.loadJSON(data);
                        jitwidget.compute();
                        jitwidget.plot();
                    });
              }
         })""")

