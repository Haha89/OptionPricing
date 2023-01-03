from math import exp
from models import BaseOption, Environment
from scipy.stats import norm
from datetime import date


class Put(BaseOption):

    def __init__(self, strike: float, maturity: date, underlying: str, environment: Environment):
        super().__init__(strike, maturity, underlying, environment)
        self.opt_type = "C"

    def price_with_black_scholes(self, vol=None):
        d1, d2 = self.get_d1_and_d2(vol)
        e1 = self.spot * norm.cdf(-d1)
        e2 = self.strike * exp(- self.r * self.T) * norm.cdf(-d2)
        return e2 - e1
