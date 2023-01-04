from option_vol.implied_vol_calculator import ImpliedVolCalculator
from option_vol.models import Environment
from option_vol.utils import display_options

""" Display option_vol surface for TSLA listed options using marketwatch website"""

UNDERLYING = "TSLA"
RISK_FREE_RATE = 0.01

Environment().risk_free_rate = RISK_FREE_RATE  # Discount factor used for option pricing

options = ImpliedVolCalculator().get_priced_options(UNDERLYING)
print(display_options(options))
