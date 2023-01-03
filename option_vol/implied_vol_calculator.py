from datetime import date

import pandas as pd

from option_vol.models import Environment, Put, Call


class ImpliedVolCalculator:
    def __init__(self, underlying, risk_free_rate, path_png=None):
        self.underlying = underlying
        self.env = Environment(risk_free_rate=risk_free_rate)
        self.path_png = path_png

    def main(self):
        spot = self.env.get_spot(self.underlying)
        print("Retrieving listed options from MarketWatch")
        options = self.get_listed_options()
        print(f"{len(options)} options found")
        options = options[options.strike.between(spot * .85, spot * 1.15)].reset_index(drop=True)
        print("Computing implied option_vol for options around spot")
        options["ImpliedVol"] = options.apply(lambda x: self.compute_vol(**x), axis=1)
        print("Generating plots")
        self.display_surfaces(options)

    def get_listed_options(self) -> pd.DataFrame:
        from option_vol.scrapping import Scrapping
        return Scrapping().parse_option(underlying=self.underlying)

    def compute_vol(self, option_type: str, maturity: date, strike: float, price: float) -> float:
        option_params = dict(strike=strike, maturity=maturity, underlying=self.underlying, environment=self.env)
        opt = (Call if option_type == "C" else Put)(**option_params)
        return opt.solve_implied_vol(price)

    def display_surfaces(self, implied_vol):
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        option_types = ["C", "P"]
        fig = make_subplots(cols=len(option_types), specs=[[{"type": "surface"}] * len(option_types)])
        labels = dict(xaxis_title='Maturity', yaxis_title='Strike', zaxis_title='Impl. Vol')

        for i, option_type in enumerate(option_types):
            options = implied_vol[implied_vol.option_type == option_type]
            options = options.pivot_table(index="strike", values='ImpliedVol', columns="maturity", aggfunc='first')
            fig.add_trace(go.Surface(x=options.columns, y=options.index, z=options.values, showscale=False),
                          row=1, col=i + 1)

        fig.update_layout(
            template="plotly_dark",
            margin=dict(r=10, t=25, b=40, l=60),
            annotations=[dict(text="Source: marketwatch", showarrow=False)],
            scene=labels,
            scene2=labels,
            width=1500, height=1000
        )
        if self.path_png:
            fig.write_image(self.path_png)
        fig.show()
