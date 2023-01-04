from datetime import date

from option_vol.models import Call, Environment, Put
from option_vol.utils import display_options

e1 = Environment()
e1.risk_free_rate = 0.1

print(f"Spot TSLA: {e1.get_spot('TSLA')}")

call = Call(strike=85., maturity=date(2023, 1, 6), underlying='TSLA')
call.find_price()
call.set_implied_volatility()
call.set_greeks()

put = Put(strike=120., maturity=date(2023, 1, 6), underlying='TSLA')
put.find_price()
put.set_implied_volatility()
put.set_greeks()

print(display_options([call, put]))
