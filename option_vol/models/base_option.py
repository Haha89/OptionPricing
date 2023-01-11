import datetime
from datetime import date
from math import log, sqrt, exp

from scipy.stats import norm

from option_vol.models import Environment
from option_vol.utils import display_options


class BaseOption:

    def __init__(self, strike: float, maturity: date, underlying: str, price=None):
        self.type = self.__class__.__name__
        self.underlying = underlying
        self.strike = strike
        self.maturity = maturity
        self.price = price

        self.name = self.get_name()
        self.implied_vol = None
        self.T = (self.maturity - datetime.date.today()).days / 252
        self.r = Environment().risk_free_rate
        self.spot = Environment().get_spot(self.underlying)
        self.div_yield = Environment().get_div_yield(self.underlying)
        self.sqrt_t = sqrt(self.T)
        self.exp_rt = exp(- self.r * self.T)
        self.exp_div = exp(- self.div_yield * self.T)

        self.cache_d1 = {}

        for g in ["delta", "gamma", "theta", "vega", "rho"]:  # Greeks
            self.__setattr__(g, 0)

    def __eq__(self, other):
        # Two options are equal if same type, strike, maturity and underlying
        return self.type == other.type and self.strike == other.strike and \
            self.maturity == other.maturity and self.underlying == other.underlying

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return str(display_options([self]))

    def get_name(self):
        und, mat, typ = self.underlying, self.maturity.strftime('%y%m%d'), self.type[0]
        return f"{und}{mat}{typ}{self.strike:09.3f}".replace('.', '')

    def price_with_black_scholes(self, vol: float) -> float:
        """ Placeholder, """
        print("This function should not be called directly")
        return vol

    def get_d1(self, vol) -> float:
        if vol not in self.cache_d1:
            self.cache_d1[vol] = (1 / vol * self.sqrt_t) * (
                    log(self.spot / self.strike) + self.T * (self.r - self.div_yield + .5 * vol ** 2))
        return self.cache_d1[vol]

    def get_d2(self, vol) -> float:
        return self.get_d1(vol) - vol * self.sqrt_t

    def get_d1_and_d2(self, vol) -> (float, float):
        d1 = self.get_d1(vol=vol)
        d2 = d1 - vol * self.sqrt_t
        return d1, d2

    def get_gamma(self) -> float:
        return self.exp_div * norm.pdf(self.get_d1(vol=self.implied_vol)) / (
                self.spot * self.implied_vol * self.sqrt_t)

    def get_vega(self, vol=None) -> float:
        """ calculates the vega of an option using the Black-Scholes model, given the volatility.
        It corresponds to the rate of change of the price of an option with respect to the volatility """
        v = vol or self.implied_vol
        return self.spot * self.sqrt_t * self.exp_div * norm.pdf(self.get_d1(vol=v))

    def set_implied_volatility(self) -> float:
        if not self.implied_vol:
            self.implied_vol = self.solve_implied_vol(self.price)
        return self.implied_vol

    def solve_implied_vol(self, target_price, max_iter=100, tol=1e-5, initial_vol=0.2) -> float:
        """  Uses the Newton-Raphson method to find the implied volatility that would produce an option price closest
        to the target price."""
        vol = initial_vol
        for i in range(max_iter):
            price = self.price_with_black_scholes(vol=vol)
            vega = self.get_vega(vol=vol)
            vol_prev = vol
            vol -= (price - target_price) / vega
            change = abs(vol - vol_prev)
            if change < tol:
                return vol
            if change > 2 * tol and i > 1:
                break
        return vol

    def set_greeks(self):
        """ calculate greeks values (sensitivity of an option value to underlying price,
         volatility, time and interest rate) of the option only once and store it as a object attribute for future use """
        for g in ["delta", "gamma", "theta", "rho", "vega"]:  # Greeks
            if not getattr(self, f"{g}"):
                greek = getattr(self, f"get_{g}")()
                setattr(self, g, greek)

    def find_price(self):
        listed_options = Environment().get_listed_options(self.underlying)
        if found_options := list(filter(lambda x: x == self, listed_options)):  # Could use the name also
            self.price = found_options[0].price
            return self.price
        else:  # No listed option found, lets approximate price with close listed options
            pass
