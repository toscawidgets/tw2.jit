
from tw2.jit.widgets import AreaChart
from tw2.jit.widgets import BarChart
from tw2.jit.widgets import PieChart

from tw2.jit.defaults import AreaChartJSONDefaults
from tw2.jit.defaults import BarChartJSONDefaults
from tw2.jit.defaults import PieChartJSONDefaults

class DemoAreaChart(AreaChart):
    data = AreaChartJSONDefaults

class DemoBarChart(BarChart):
    data = BarChartJSONDefaults

class DemoPieChart(PieChart):
    data = PieChartJSONDefaults
    sliceOffset = 5 
