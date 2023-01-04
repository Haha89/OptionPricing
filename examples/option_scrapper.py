import pandas as pd

from option_vol.implied_vol_calculator import ImpliedVolCalculator

""" Display listed options for TSLA using marketwatch website"""

UNDERLYING = "TSLA"

options = ImpliedVolCalculator().get_listed_options(UNDERLYING)
options = [(o.get_name(), o.__class__.__name__, o.strike, o.maturity, o.price) for o in options]
print(pd.DataFrame(options, columns=["Name", "Type", "Strike", "Maturity", "Price"]))
