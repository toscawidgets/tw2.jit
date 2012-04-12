import tw2.core as twc
from tw2.core.resources import JSSymbol, CSSLink

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_css, modname

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

    offset = twc.Param(
        '(number) Margin between boxes.', default=2, attribute=True)

    cushion = twc.Param(
        '(boolean) Cushion Gradients', default=False, attribute=True)

    titleHeight = twc.Param(
        '(number) The height of the title rectangle for non-leaf nodes.',
        default=13, attribute=True)

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
            'onClick': JSSymbol(src='(function(node) {if (node) {$$jitwidget.enter(node);}})'),
            'onRightClick': JSSymbol(src='(function() {$$jitwidget.out();})'),
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
        '(number) A number in the range [0, 1) that will be subtracted to ' +
        'each node position to make a more compact HyperTree.  This will ' +
        'avoid placing nodes too far from each other when there is a ' +
        'selected node.',
        default=0, attribute=True)

class SpaceTree(JitTree):
    """ A Tree layout with advanced contraction and expansion animations.

    See thejit API documentation on SpaceTree:
        http://thejit.org/static/v20/Docs/files/Visualizations/Spacetree-js.html
    """

    jitClassName = 'ST'

    transition = twc.Param(
        '(javascript) Javascript to perform transition.',
        default=JSSymbol(src='$jit.Trans.Quart.easeInOut'), attribute=True)

    levelDistance = twc.Param(
        '(number) The distance between two consecutive levels of the tree.',
        default=30, attribute=True)

    offsetX = twc.Param(
        '(number) The x-offset distance from the' +
        'selected node to the center of the canvas.',
        default=0, attribute=True)

    offsetY = twc.Param(
        '(number) The y-offset distance from the' +
        'selected node to the center of the canvas.',
        default=0, attribute=True)

class Icicle(JitTree):
    """ Icicle space filling visualization.

    See thejit API documentation on Icicle:
        http://thejit.org/static/v20/Docs/files/Visualizations/Icicle-js.html
    """

    jitClassName = 'Icicle'

    offset = twc.Param('(number) Boxes offset', default=2, attribute=True)

