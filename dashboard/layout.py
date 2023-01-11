from dash import dcc, html
from dash.dash_table import DataTable

from dashboard.constants import UNDERLYINGS, TYPES, METRICS


def set_layout(app):
    return html.Div(
        children=[
            html.Div(
                className="row",
                children=[
                    # Column for user controls
                    html.Div(
                        className="four columns div-user-controls",
                        children=[
                            html.A(
                                html.Img(
                                    className="logo",
                                    src=app.get_asset_url("dash-logo-new.png"),
                                ),
                                href="https://plotly.com/dash/",
                            ),
                            html.H2("OPTIONS METRIC VIEWER"),
                            html.P(
                                """Select an underlying, an option type and a metric using the pickers below:"""
                            ),

                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="div-for-dropdown",
                                        children=get_dropdown("underlying", UNDERLYINGS)),

                                    html.Div(
                                        className="div-for-dropdown",
                                        children=get_dropdown("type", TYPES)),

                                    html.Div(
                                        className="div-for-dropdown",
                                        children=get_dropdown("metric", METRICS)),

                                    html.Div(
                                        className="text-padding",
                                        children=[
                                            "Range around spot (+/- X%)"
                                        ],
                                    ),
                                    html.Div(
                                        className="div-for-dropdown",
                                        children=[dcc.Slider(min=10, max=50, step=10, value=20, id='slider-range')]),

                                    html.P(id="underlying-spot"),
                                    html.P(id="total-options"),
                                ],
                            ),
                            dcc.Markdown(
                                """
                                Source: [MarketWatch](https://www.marketwatch.com/)
                                """
                            ),
                        ],
                    ),
                    html.Div(
                        className="eight columns div-for-charts bg-grey",
                        children=[
                            dcc.Graph(id="metric-surface"),
                            html.Div(
                                className="text-padding",
                                children=[
                                    "Listed options found in Marketwatch"
                                ],
                            ),
                            DataTable(id="listed-options-table", page_size=13,
                                      sort_action="native",
                                      style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
                                      style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
                                      ),
                        ],
                    )
                ],
            )
        ]
    )


def get_dropdown(name, values):
    """
    Returns a Dash dropdown element with options passed as list or dictionary.
    Raises error if options passed are not list or dictionary
    """
    if isinstance(values, dict):
        options = [{"label": k, "value": v} for k, v in values.items()]
    elif isinstance(values, list):
        options = [{"label": i, "value": i} for i in values]
    else:
        raise ValueError(f"values cannot be of type {type(values)}")
    placeholder = f"{name.title()} selection"
    return [dcc.Dropdown(id=f"{name}-dropdown", options=options, value=options[0]["value"], placeholder=placeholder)]
