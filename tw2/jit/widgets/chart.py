import tw2.core as twc
from tw2.jit.widgets.core import JitWidget

class JitChart(JitWidget):
    """ Baseclass common to all chart widgets """
    type = twc.Param(
        '(string) Stack style.  Possible values are ' +
        '"stacked", "stacked:gradient" to add gradients.',
        default='stacked:gradient', attribute=True)

    showLabels = twc.Param(
        '(boolean) Display the slot names.', default=True, attribute=True)

    labelOffset = twc.Param(
        '(number) Adds margin between the label and the ' +
        'default place where it should be drawn.',
        default=3, attribute=True)

class AreaChart(JitChart):
    """ A visualization that displays stacked area charts.

    See thejit API documentation on AreaChart:
        http://thejit.org/static/v20/Docs/files/Visualizations/AreaChart-js.html
    """

    jitClassName = 'AreaChart'

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


class BarChart(JitChart):
    """ A visualization that displays stacked bar charts.

    See thejit API documentation on BarChart:
        http://thejit.org/static/v20/Docs/files/Visualizations/BarChart-js.html
    """

    jitClassName = 'BarChart'

    barsOffset = twc.Param(
        '(number) Separation between bars.', default=0, attribute=True)

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


class PieChart(JitChart):
    """ A visualization that displays stacked pie charts.

    See thejit API documentation on PieChart:
        http://thejit.org/static/v20/Docs/files/Visualizations/PieChart-js.html
    """

    jitClassName = 'PieChart'

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

