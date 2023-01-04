from datetime import date
from math import exp, sqrt

from scipy.stats import norm

from option_vol.models import BaseOption


class Call(BaseOption):

    def __init__(self, strike: float, maturity: date, underlying: str, price=None):
        super().__init__(strike, maturity, underlying, price)

    def price_with_black_scholes(self, vol=None):
        d1, d2 = self.get_d1_and_d2(vol)
        e1 = self.spot * exp(- self.div_yield * self.T) * norm.cdf(d1)
        e2 = self.strike * exp(- self.r * self.T) * norm.cdf(d2)
        return e1 - e2

    def get_delta(self):
        return exp(- self.div_yield * self.T) * norm.cdf(self.get_d1(self.implied_vol))

    def get_theta(self):
        d1, d2 = self.get_d1_and_d2(self.implied_vol)
        a = (self.spot * norm.pdf(d1) * self.implied_vol * exp(- self.div_yield * self.T)) / (2 * sqrt(self.T))
        b = self.r * self.strike * exp(- self.r * self.T) * norm.cdf(d2)
        c = self.div_yield * self.spot * exp(- self.div_yield * self.T) * norm.cdf(d1)
        return (1 / self.T) * (-a - b + c)

    def get_rho(self):
        return .01 * self.strike * self.T * exp(- self.r * self.T) * norm.cdf(self.get_d2(self.implied_vol))
