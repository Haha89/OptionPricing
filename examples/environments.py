from option_vol.models import Environment

e1 = Environment()
e1.risk_free_rate = 0.1

print(f"Spot TSLA: {e1.get_spot('TSLA')}")
print(f"Risk free rate: {e1.risk_free_rate}")
print(f"Spot SPX: {e1.get_spot('SPX')}")