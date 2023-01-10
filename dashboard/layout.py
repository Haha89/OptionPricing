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
                                        children=[
                                            dcc.Dropdown(
                                                id="underlying-dropdown",
                                                options=[{"label": i, "value": i} for i in UNDERLYINGS],
                                                value=UNDERLYINGS[0],
                                                placeholder="Select an underlying",
                                            )
                                        ],
                                    ),
                                    html.Div(
                                        className="div-for-dropdown",
                                        children=[
                                            dcc.Dropdown(
                                                id="type-dropdown",
                                                options=[{"label": i, "value": i} for i in TYPES],
                                                value=TYPES[0],
                                                placeholder="Select a type",
                                            )
                                        ],
                                    ),
                                    html.Div(
                                        className="div-for-dropdown",
                                        children=[
                                            dcc.Dropdown(
                                                id="metric-dropdown",
                                                options=[{"label": k, "value": v} for k, v in METRICS.items()],
                                                value=list(METRICS.values())[0],
                                                placeholder="Select a metric",
                                            )
                                        ],
                                    ),
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
                    ),
                ],
            )
        ]
    )
