import pandas as pd
from dash import Input, Output

from dashboard.constants import metrics
from option_vol.implied_vol_calculator import ImpliedVolCalculator
from option_vol.plotting import Plotting
from option_vol.utils import list_to_df, to_title


def assign_callbacks(app):
    @app.callback(
        [Output("underlying-spot", "children"), Output("total-options", "children"),
         Output("listed-options-table", "data"), Output("metric-surface", "figure")],
        [Input("underlying-dropdown", "value"), Input("type-dropdown", "value"),
         Input("metric-dropdown", "value"), Input("slider-range", "value")],
    )
    def update_output(underlying, _type, metric, depth):
        """ Given 3 inputs, should return a tuple with the surface and the list of options"""
        if not all([underlying, _type, metric]):  # Some input is missing? Do nothing
            return ["", f"Nb options 0", pd.DataFrame().to_dict("records"),
                    {'data': [], 'layout': dict(paper_bgcolor="rgba(0,0,0,0)",
                                                plot_bgcolor="rgba(0,0,0,0)",
                                                font={"color": "white"})}]
        else:
            from option_vol.models import Environment
            env = Environment()
            env.risk_free_rate = 0.1

            spot = round(env.get_spot(underlying), 2)
            print("Retrieving listed options from MarketWatch")
            cols = ["name", "strike", "maturity"] + metrics

            options = ImpliedVolCalculator().get_priced_options(underlying, depth)
            options = list(filter(lambda o: o.type == _type, options))
            surface = Plotting.get_surface(options, metric)
            print("Sending updates")
            table_options = list_to_df(options)[cols].rename(
                columns=dict(zip(cols, list(map(to_title, cols))))).to_dict("records")
            return [f"{underlying} spot: {spot}", f"Nb options {len(options)}",
                    table_options, surface]
