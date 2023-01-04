from datetime import date
from math import exp, sqrt

from scipy.stats import norm

from option_vol.models import BaseOption


class Put(BaseOption):

    def __init__(self, strike: float, maturity: date, underlying: str, price=None):
        super().__init__(strike, maturity, underlying, price)

    def price_with_black_scholes(self, vol=None) -> float:
        d1, d2 = self.get_d1_and_d2(vol)
        e1 = self.spot * exp(- self.div_yield * self.T) * norm.cdf(-d1)
        e2 = self.strike * exp(- self.r * self.T) * norm.cdf(-d2)
        return e2 - e1

    def get_delta(self) -> float:
        return exp(- self.div_yield * self.T) * (norm.cdf(self.get_d1(self.implied_vol)) - 1)

    def get_theta(self) -> float:
        d1, d2 = self.get_d1_and_d2(self.implied_vol)
        a = (self.spot * norm.pdf(d1) * self.implied_vol * exp(- self.div_yield * self.T)) / (2 * sqrt(self.T))
        b = self.r * self.strike * exp(- self.r * self.T) * norm.cdf(-d2)
        c = self.div_yield * self.spot * exp(- self.div_yield * self.T) * norm.cdf(-d1)
        return (-a + b - c) / 252

    def get_rho(self) -> float:
        return -.01 * self.strike * self.T * exp(- self.r * self.T) * norm.cdf(-self.get_d2(self.implied_vol))
