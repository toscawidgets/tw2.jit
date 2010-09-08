import tw2.core as twc
from tw2.core.resources import JSSymbol, CSSLink

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js, jit_css, modname

from tw2.jit.defaults import TreeMapJSONDefaults
from tw2.jit.defaults import SunburstJSONDefaults
from tw2.jit.defaults import IcicleJSONDefaults
from tw2.jit.defaults import SpaceTreeJSONDefaults
from tw2.jit.defaults import HyperTreeJSONDefaults

treemap_css = CSSLink(modname=modname, filename="static/css/Treemap.css")
sunburst_css = CSSLink(modname=modname, filename="static/css/Sunburst.css")

class JitTree(JitTreeOrGraphWidget):
    """ Baseclass common to all jit tree widgets """

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
    """ A squarified TreeMap visualization.

    'Strip' and 'SliceAndDice' variations not yet supported.

    See thejit API documentation on TreeMap:
        http://thejit.org/static/v20/Docs/files/Visualizations/Treemap-js.html
    """

    def prepare(self):
        super(TreeMap, self).prepare()
        self.resources.extend([jit_css, treemap_css])
    
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
    """ A radial space filling tree visualization.

    See thejit API documentation on Sunburst:
        http://thejit.org/static/v20/Docs/files/Visualizations/Sunburst-js.html
    """
    def prepare(self):
        super(Sunburst, self).prepare()
        self.resources.extend([jit_css, sunburst_css])

    jitClassName = 'Sunburst'

    levelDistance = twc.Param(
        '(number) Distance between levels.',
        default=90, attribute=True, request_local=False)

class HyperTree(JitTree):
    """ A Hyperbolic Tree/Graph visualization.

    See thejit API documentation on HyperTree:
        http://thejit.org/static/v20/Docs/files/Visualizations/Hypertree-js.html
    """

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
    """ A Tree layout with advanced contraction and expansion animations.

    See thejit API documentation on SpaceTree:
        http://thejit.org/static/v20/Docs/files/Visualizations/Spacetree-js.html
    """

    jitClassName = 'ST'
   
    transition = twc.Param(
        'javascript _TODO',
        default=JSSymbol(src='$jit.Trans.Quart.easeInOut'),
        attribute=True, request_local=False)

    levelDistance = twc.Param(
        'foo TODO',
        default=50, attribute=True, request_local=False)

class Icicle(JitTree):
    """ Icicle space filling visualization.

    See thejit API documentation on Icicle:
        http://thejit.org/static/v20/Docs/files/Visualizations/Icicle-js.html
    """

    jitClassName = 'Icicle'
