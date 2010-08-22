import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.core import JitTreeOrGraphWidget
from tw2.jit.widgets.core import jit_js

from tw2.jit.defaults import ForceDirectedGraphJSONDefaults

# TODO -- PANIC -- what should thsi include from JitChart??? or JitTree?
class JitGraph(JitTreeOrGraphWidget):
    pass

#Radial Graph
class RadialGraph(JitGraph):
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(default='RGraph')

    background = twc.Param(
        '(dict) see sample (TODO).', default={},
        attribute=True, request_local=False)
   
class ForceDirectedGraph(JitGraph):
    template = "genshi:tw2.jit.templates.jitwidget"
    
    jitClassName = twc.Variable(default='ForceDirected')
    
    iterations = twc.Param(
        '(number) The number of iterations for the spring ' +
        'layout simulation.  Depending on the browser\'s ' +
        'speed you could set this to a more "interesting" ' +
        'number, like 200.',
        default=2, attribute=True, request_local=False)
    
    levelDistance = twc.Param(
        '(number) The natural length desired for the edges.',
        default=50, attribute=True, request_local=False)

