from datetime import date

from scipy.stats import norm

from option_vol.models import BaseOption


class Call(BaseOption):

    def __init__(self, strike: float, maturity: date, underlying: str, price=None):
        super().__init__(strike, maturity, underlying, price)

    def price_with_black_scholes(self, vol=None) -> float:
        d1, d2 = self.get_d1_and_d2(vol)
        e1 = self.spot * self.exp_div * norm.cdf(d1)
        e2 = self.strike * self.exp_rt * norm.cdf(d2)
        return e1 - e2

    def get_delta(self) -> float:
        return self.exp_div * norm.cdf(self.get_d1(self.implied_vol))

    def get_theta(self) -> float:
        d1, d2 = self.get_d1_and_d2(self.implied_vol)
        a = (self.spot * norm.pdf(d1) * self.implied_vol * self.exp_div) / (2 * self.sqrt_t)
        b = self.r * self.strike * self.exp_rt * norm.cdf(d2)
        c = self.div_yield * self.spot * self.exp_div * norm.cdf(d1)
        return (-a - b + c) / 252

    def get_rho(self) -> float:
        return .01 * self.strike * self.T * self.exp_rt * norm.cdf(self.get_d2(self.implied_vol))
