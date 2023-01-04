from os import path

from option_vol.implied_vol_calculator import ImpliedVolCalculator
from option_vol.models import Environment

""" Display option_vol surface for TSLA listed options using marketwatch website"""

UNDERLYING = "TSLA"
RISK_FREE_RATE = 0.01
PATH_PNG = fr"..\images\vol_surface_{UNDERLYING}.png"

Environment().risk_free_rate = RISK_FREE_RATE  # Discount factor used for option pricing

ImpliedVolCalculator().get_implied_vol_surface(UNDERLYING, path.abspath(PATH_PNG))
