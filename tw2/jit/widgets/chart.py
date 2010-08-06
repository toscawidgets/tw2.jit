import tw2.core as twc
from tw2.jit.widgets.core import JitWidget

from tw2.jit.defaults import AreaChartJSONDefaults
from tw2.jit.defaults import BarChartJSONDefaults
from tw2.jit.defaults import PieChartJSONDefaults

class JitChart(JitWidget):
    type = twc.Param(
        '(string) Stack style.  Possible values are ' + 
        '"stacked", "stacked:gradient" to add gradients.',
        default='stacked:gradient', attribute=True)
    showLabels = twc.Param(
        '(boolean) Display the slot names.', default=True, attribute=True)
    labelOffset = twc.Param(
        '(number) Adds margin between the label and the ' +
        'default place where it should be drawn.', default=3, attribute=True)

class AreaChart(JitChart):
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(default='AreaChart')
    
    data = twc.Param(default=AreaChartJSONDefaults)

    selectOnHover = twc.Param(
        '(boolean) Add a mark to the hovered stack.',
        default=True, attribute=True)
    
    filterOnClick = twc.Param(
        '(boolean) Select the clicked stack and hide others.',
        default=True, attribute=True)

    restoreOnRightClick = twc.Param(
        '(boolean) Show all stacks by right clicking.',
        default=True, attribute=True)
    
    showAggregates = twc.Param(
        '(boolean) Display the sum of the stack values.',
        default=True, attribute=True)

    # TODO -- not actually a new requisite of AreaChart
    # TODO -- how to handle the black background always passed to the template?
    Label = twc.Param(
        'dictionary of parameters for the labels', attribute=True,
        default={
            'type' : 'Native',
            'size' : 20,
            'family' : 'Arial',
            'color' : 'white'
        })


class BarChart(JitChart):
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(default='BarChart')
    
    data = twc.Param(default=BarChartJSONDefaults)
    
    barsOffset = twc.Param(
        '(number) Separation between bars.',
        default=0, attribute=True)

    hoveredColor = twc.Param(
        '(string) The color for a hovered bar stack.',
        default='#9fd4ff', attribute=True)

    orientation = twc.Param(
        '(string) The direction of the bars.  ' + 
        'Possible options are "vertical" and "horizontal".',
        default='horizontal', attribute=True)
    
    showAggregates = twc.Param(
        '(boolean) Display the sum of the stack values.',
        default=True, attribute=True)

    # TODO ditch this as above...
    Label = twc.Param(
        'dictionary of parameters for the labels', attribute=True,
        default={
            'type' : 'Native',
            'size' : 20,
            'family' : 'Arial',
            'color' : 'white'
        })


class PieChart(JitChart):
    template = "genshi:tw2.jit.templates.jitwidget"

    jitClassName = twc.Variable(default='PieChart')
    
    data = twc.Param(default=PieChartJSONDefaults)

    sliceOffset = twc.Param(
        '(number) Separation between slices.', default=0, attribute=True)

    hoveredColor = twc.Param(
        '(string) Sets the selected color for a hovered pie stack.',
        default='#9fd4ff', attribute=True)

    resizeLabels = twc.Param(
        '(boolean|number) Resize the pie labels according to ' +
        'their stacked values.  Set a number for resizeLabels ' +
        'to set a font size minimum.',
        default=False, attribute=True)

    updateHeights = twc.Param(
        '(boolean) Only for mono-valued (most common) pie ' +
        'charts.  Resize the height of the pie slices ' +
        'according to their current values.',
        default=False, attribute=True)
   
    # TODO -- get rid of this
    Label = twc.Param(
        'dictionary of parameters for the labels',
        default={
            'type' : 'Native',
            'size' : 20,
            'family' : 'Arial',
            'color' : 'white'
        }, attribute=True)

