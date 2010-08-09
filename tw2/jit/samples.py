
from tw2.jit.widgets import AreaChart
from tw2.jit.widgets import BarChart
from tw2.jit.widgets import PieChart
from tw2.jit.widgets import RadialGraph

from tw2.jit.defaults import AreaChartJSONDefaults
from tw2.jit.defaults import BarChartJSONDefaults
from tw2.jit.defaults import PieChartJSONDefaults
from tw2.jit.defaults import RadialGraphJSONDefaults

class DemoAreaChart(AreaChart):
    data = AreaChartJSONDefaults

class DemoBarChart(BarChart):
    data = BarChartJSONDefaults

class DemoPieChart(PieChart):
    data = PieChartJSONDefaults
    sliceOffset = 5 

class DemoRadialGraph(RadialGraph):
    data = RadialGraphJSONDefaults
    postinitJS = """
            //trigger small animation for kicks
            jitwidget.graph.eachNode(function(n) {
                var pos = n.getPos();
                pos.setc(-200, -200);
            });
            jitwidget.compute('end');
            jitwidget.fx.animate({
                modes:['polar'],
                duration: 2000
            });"""

