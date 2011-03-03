""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import AreaChart
from tw2.jit.samples.samples_data import AreaChartJSONSampleData
class DemoAreaChart(AreaChart):
    """ This is the only sample that loads its data asynchronously """
    offset = 0
    labelOffset = 15
    showAggregates = True
    showLabels = True
    type = 'stacked'
    Label = {
        'type': 'Native',
        'size': 15,
        'family': 'Arial',
        'color': 'white'
    }
    Tips = {
        'enable': True,
        'onShow' : JSSymbol(src="""
        (function(tip, elem) {
            tip.innerHTML = "<b>" + elem.name + "</b>: $" + elem.value + " per year income (adjusted for inflation)";
        })""")
    }

    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        return AreaChartJSONSampleData
    base_url = '/area_chart_data/'

import tw2.core as twc
twc.core.request_local()['middleware'].controllers.register(DemoAreaChart,
                                                            'area_chart_data')

from tw2.jit.widgets import BarChart
from tw2.jit.samples.samples_data import BarChartJSONSampleData
class DemoBarChart(BarChart):
    data = BarChartJSONSampleData


from tw2.jit.widgets import PieChart
from tw2.jit.samples.samples_data import PieChartJSONSampleData
class DemoPieChart(PieChart):
    data = PieChartJSONSampleData
    sliceOffset = 5 
