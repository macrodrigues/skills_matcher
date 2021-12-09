#shows gauge meter for recruiter side of the project
#belongs to skills_matcher/scripts/utils/
import plotly.graph_objects as go


def gauge_meter(var):
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(value=var,
                        gauge={'axis': {
                            'visible': False
                        }},
                        domain={
                            'row': 0,
                            'column': 0
                        }))

    fig.update_layout(grid={
        'rows': 2,
        'columns': 2,
        'pattern': "independent"
    },
                        template={
                            'data': {
                                'indicator': [{
                                    'title': {
                                        'text': "Fit"
                                    },
                                    'mode':
                                    "number+delta+gauge"
                                }]
                            }
                        })

    return fig
