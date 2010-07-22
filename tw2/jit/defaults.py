# This module just contains some of the more lengthy constants used in
# widgets.py that would otherwise clutter that file.
AreaChartJSONDefaults = {
    'label': ['label A', 'label B', 'label C', 'label D'],
    'values': [
        {
            'label': 'date A',
            'values': [20, 40, 15, 5]
        },
        {
            'label': 'date B',
            'values': [30, 10, 45, 10]
        },
        {
            'label': 'date E',
            'values': [38, 20, 35, 17]
        },
        {
            'label': 'date F',
            'values': [58, 10, 35, 32]
        },
        {
            'label': 'date D',
            'values': [55, 60, 34, 38]
        },
        {
            'label': 'date C',
            'values': [26, 40, 25, 40]
        }
    ]
}
BarChartJSONDefaults = AreaChartJSONDefaults
PieChartJSONDefaults = AreaChartJSONDefaults
