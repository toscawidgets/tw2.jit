import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget

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

    levelDistance = twc.Param(
        '(number) Distance between levels',
        default=100, attribute=True, request_local=False)

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
