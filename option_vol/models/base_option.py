import datetime
from datetime import date
from math import log, sqrt, exp

from scipy.stats import norm

from option_vol.models import Environment


class BaseOption:

    def __init__(self, strike: float, maturity: date, underlying: str, price=None):
        self.implied_vol = None
        self.strike = strike
        self.maturity = maturity
        self.underlying = underlying
        self.price = price

        self.T = (self.maturity - datetime.date.today()).days / 365
        self.r = Environment().risk_free_rate
        self.spot = Environment().get_spot(self.underlying)
        self.div_yield = Environment().get_div_yield(self.underlying)

        for g in ["delta", "gamma", "theta", "vega", "rho"]:  # Greeks
            self.__setattr__(g, 0)

    def __str__(self):
        return self.get_name()

    def get_name(self):
        und, mat, typ = self.underlying, self.maturity.strftime('%y%m%d'), self.__class__.__name__[0]
        return f"{und}{mat}{typ}{self.strike:09.3f}".replace('.', '')

    def price_with_black_scholes(self, vol: float):
        """ Placeholder, """
        print("This function should not be called directly")
        return vol

    def get_d1(self, vol):
        return (1 / vol * sqrt(self.T)) * (
                log(self.spot / self.strike) + self.T * (self.r - self.div_yield + .5 * vol ** 2))

    def get_d2(self, vol):
        return self.get_d1(vol) - vol * sqrt(self.T)

    def get_d1_and_d2(self, vol):
        d1 = self.get_d1(vol=vol)
        d2 = d1 - vol * sqrt(self.T)
        return d1, d2

    def get_gamma(self):
        return exp(- self.div_yield * self.T) * norm.pdf(self.get_d1(vol=self.implied_vol)) / (self.spot * self.implied_vol * sqrt(self.T))

    def get_vega(self, vol=None):
        return self.spot * sqrt(self.T) * exp(- self.div_yield * self.T) * norm.pdf(self.get_d1(vol=vol))

    def set_implied_volatility(self, target_price):
        self.implied_vol = self.solve_implied_vol(target_price)

    def solve_implied_vol(self, target_price):
        """ Use Newton-Raphson to solve BS(v) - target_price = 0 """
        max_iter, tolerance, vol = 100, 1e-5, 0.5
        for _ in range(max_iter):
            price = self.price_with_black_scholes(vol=vol)
            if abs(price - target_price) < tolerance:
                return vol
            vol -= (price - target_price) / self.get_vega(vol=vol)
        return vol

    def set_greeks(self):
        for g in ["delta", "gamma", "theta", "rho"]:  # Greeks
            greek = getattr(self, f"get_{g}")()
            setattr(self, g, greek)
