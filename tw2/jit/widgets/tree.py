import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js, jit_css, treemap_css, sunburst_css

from tw2.jit.defaults import TreeMapJSONDefaults
from tw2.jit.defaults import SunburstJSONDefaults
from tw2.jit.defaults import IcicleJSONDefaults
from tw2.jit.defaults import SpaceTreeJSONDefaults
from tw2.jit.defaults import HyperTreeJSONDefaults


class JitTree(JitTreeOrGraphWidget):
    constrained = twc.Param(
        '(boolean) Whether to show the entire tree when loaded ' +
        'or just the number of levels specified by levelsToShow.',
        default=False, attribute=True)
    levelsToShow = twc.Param(
        '(number) The number of levels to show for a subtree.  This ' +
        'number is relative to the selected node.',
        default=3, attribute=True)
   
    # TODO -- wait what?  which tree children do these belong to?
    offset = twc.Param(
        '(number)', default=1, attribute=True, request_local=False)

    cushion = twc.Param(
        '(boolean)', default=1, attribute=True, request_local=False)

    constrained = twc.Param(
        '(boolean)', default=True, attribute=True, request_local=False)

    levelsToShow = twc.Param(
        '(number)', default=3, attribute=True, request_local=False)

class TreeMap(JitTree):
    def prepare(self):
        super(TreeMap, self).prepare()
        self.resources.extend([jit_css, treemap_css])
    
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = 'TM'
    jitSecondaryClassName = 'Squarified'

    # Just a note -- this is different from the parents' "offset"
    #  Bad thejit.. bad.
    offset = twc.Param(
        '(number) Margin between boxes.', default=0, attribute=True)
    
    orientation = twc.Param(
        '(string) Whether to set horizontal or vertical layout.  ' +
        'Possible values are "h" or "v".', default='h', attribute=True)

    titleHeight = twc.Param(
        '(number) Separation between the center of the ' +
        'canvas and each pie slice.', default=13, attribute=True)
   
    Events = twc.Param(
        '(dict) Of the form Options.Events in the jit docs.',
        default={
            'enable': True,
            'onClick': JSSymbol(src='(function(node) {if (node) {jitwidget.enter(node);}})'),
            'onRightClick': JSSymbol(src='(function() {jitwidget.out();})'),
        }, attribute=True)

    # TODO - Node.Type 
    #see http://thejit.org/static/v20/Docs/files/Visualizations/Treemap-js.html

class Sunburst(JitTree):
    def prepare(self):
        super(Sunburst, self).prepare()
        self.resources.extend([jit_css, sunburst_css])

    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = 'Sunburst'

    levelDistance = twc.Param(
        '(number) Distance between levels.',
        default=90, attribute=True, request_local=False)

class HyperTree(JitTree):
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = 'Hypertree'
    
    w = twc.Variable( 'width of the canvas.', default=500 )
    h = twc.Variable( 'height of the canvas.', default=500 )
    
    def prepare(self):
        super(HyperTree, self).prepare()
        self.w = self.width
        self.h = self.height

    
    offset = twc.Param(
        '(number)', default=0, attribute=True, request_local=False)

class SpaceTree(JitTree):
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = 'ST'
   
    transition = twc.Param(
        'javascript _TODO',
        default=JSSymbol(src='$jit.Trans.Quart.easeInOut'),
        attribute=True, request_local=False)

    levelDistance = twc.Param(
        'foo TODO',
        default=50, attribute=True, request_local=False)

class Icicle(JitTree):
    resources = [jit_js]
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(default='Icicle')
    
    data = twc.Param(default=IcicleJSONDefaults)

    postinitJS = twc.Param(
        default="jitwidget.refresh();", attribute=True, request_local=False)

    Tips = twc.Param(
        '(dict)',
        default={
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
            })""")}, attribute=True, request_local=False)
    Events = twc.Param(
        default= {
            'enable': True,
            'onMouseEnter': JSSymbol(src="""
            (function(node) {
                node.setData('border', '#33dddd');
                jitwidget.fx.plotNode(node, jitwidget.canvas);
                jitwidget.labels.plotLabel(jitwidget.canvas, node, jitwidget.controller);
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
      }, attribute=True, request_local=False)
    onCreateLabel = twc.Param(
         '(string) javascript callback.',
         default=JSSymbol(src="""
         (function(domElement, node){
              domElement.innerHTML = node.name;
              var style = domElement.style;
              style.fontSize = '0.9em';
              style.display = '';
              style.cursor = 'pointer';
              style.color = '#333';
              style.overflow = 'hidden';
        })"""), attribute=True, request_local=False)
    onPlaceLabel = twc.Param(
         '(string) javascript callback.',
         default=JSSymbol(src="""
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
        })"""), attribute=True, request_local=False)

