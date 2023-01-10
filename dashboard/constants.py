from option_vol.utils import to_title

TYPES = ["Call", 'Put']
UNDERLYINGS = ["TSLA", 'AAPL', 'SPX', 'AMZN']
metrics = ["implied_vol", "delta", "gamma", "price", "rho", "vega", "theta"]
METRICS = {to_title(e): e for e in metrics}
