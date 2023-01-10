import pandas as pd
from dash import Input, Output

from option_vol.plotting import Plotting
from option_vol.utils import options_to_df


def assign_callbacks(app):
    @app.callback(
        [Output("underlying-spot", "children"), Output("total-options", "children"),
         Output("listed-options-table", "data"), Output("metric-surface", "figure")],  # ],
        [Input("underlying-dropdown", "value"), Input("type-dropdown", "value"), Input("metric-dropdown", "value")],
    )
    def update_output(underlying, _type, metric):
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
            options = env.get_listed_options(underlying)
            options = list(filter(lambda o: o.type == _type, options))
            print(f"option done  {len(options)}")
            cols = ["name", "strike", "maturity", "price"]
            surface = make_surface(underlying, _type, metric)
            print("Sending updates")
            return [f"{underlying} spot: {spot}", f"Nb options {len(options)}",
                    options_to_df(options)[cols].to_dict("records"), surface]

        # https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-yield-curve/app.py


def make_surface(underlying, _type, metric):
    from option_vol.implied_vol_calculator import ImpliedVolCalculator
    options = ImpliedVolCalculator().get_priced_options(underlying)
    options = list(filter(lambda o: o.type == _type, options))
    return Plotting.get_surface(options, metric)
