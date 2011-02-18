import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js
from tw2.jit.widgets.graph import RadialGraph

class DbRadialGraph(RadialGraph):
    """ A radial graph that pulls nodes on demand.

    Based off of the following demo:
        http://demos.thejit.org/lpkgd/#

    See thejit API documentation on RadialGraph:
        http://thejit.org/static/v20/Docs/files/Visualizations/RGraph-js.html

    """

    url = twc.Param(""" TODO """)

    preprocessTree = twc.Param(
        """ TODO """,
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    requestGraph = twc.Param(
        """ TODO """,
        default=JSSymbol(src="(function(node) {})"), attribute=True)

    pass
