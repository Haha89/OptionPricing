from typing import List

from option_vol.models import Environment, BaseOption


class ImpliedVolCalculator:
    def __init__(self):
        self.env = None

    def get_priced_options(self, underlying) -> List[BaseOption]:
        self.env = Environment()
        spot = self.env.get_spot(underlying)
        print("Retrieving listed options from MarketWatch")
        options = self.env.get_listed_options(underlying)
        print(f"{len(options)} options found")
        options = [o for o in options if .85 <= o.strike / spot <= 1.15]
        print("Computing implied option_vol for options around spot")
        for o in options:
            o.set_implied_volatility()
            o.set_greeks()
        return options

    def get_implied_vol_surface(self, underlying, path_png=None):
        options = self.get_priced_options(underlying)
        print("Generating plots")
        self.display_surfaces(options, 'implied_vol', path_png)

    @staticmethod
    def display_surfaces(options: List[BaseOption], element: str, path_png):
        from option_vol.plotting import Plotting
        return Plotting().display_surfaces(options, element, path_png)
