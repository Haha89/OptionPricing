from option_vol.implied_vol_calculator import ImpliedVolCalculator

""" Display listed options for TSLA using marketwatch website"""

UNDERLYING = "TSLA"
RISK_FREE_RATE = 0.01

options = ImpliedVolCalculator(UNDERLYING, RISK_FREE_RATE).get_listed_options()
print(options.head(15))
