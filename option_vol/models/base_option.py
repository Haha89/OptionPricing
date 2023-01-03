import datetime
from math import log, sqrt
from scipy.stats import norm
from datetime import date
from option_vol.models.environment import Environment


class BaseOption:

    def __init__(self, strike: float, maturity: date, underlying: str, environment: Environment):
        self.implicit_volatility = 0
        self.strike = strike
        self.maturity = maturity
        self.underlying = underlying
        self.environment = environment
        self.r = self.environment.risk_free_rate
        self.T = (self.maturity - datetime.date.today()).days / 365
        self.spot = self.environment.get_spot(self.underlying)
        self.opt_type = "?"

    def get_name(self):
        return f"{self.underlying}{self.maturity.strftime('%y%m%d')}{self.opt_type}{self.strike:09.3f}".replace('.', '')

    def price_with_black_scholes(self, vol: float):
        """ Placeholder, """
        print("This function should not be called directly")
        return vol

    def get_d1(self, vol):
        return (1 / vol * sqrt(self.T)) * (log(self.spot / self.strike) + self.T * (self.r + .5 * vol ** 2))

    def get_d1_and_d2(self, vol):
        d1 = self.get_d1(vol=vol)
        d2 = d1 - vol * sqrt(self.T)
        return d1, d2

    def vega(self, vol=None):
        return self.spot * sqrt(self.T) * norm.cdf(self.get_d1(vol=vol))

    def set_implicit_volatility(self, target_price):
        self.implicit_volatility = self.solve_implied_vol(target_price)

    def solve_implied_vol(self, target_price):
        """ Use Newton-Raphson to solve BS(v) - target_price = 0 """
        max_iter, tolerance, vol = 100, 1e-5, 0.5
        for _ in range(max_iter):
            price = self.price_with_black_scholes(vol=vol)
            if abs(price - target_price) < tolerance:
                return vol
            vol -= (price - target_price) / self.vega(vol=vol)
        return vol
