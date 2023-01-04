from option_vol.models import Environment
from option_vol.utils import display_options

""" Display listed options for TSLA using marketwatch website"""

UNDERLYING = "TSLA"

options = Environment().get_listed_options(UNDERLYING)
print(display_options(options))
