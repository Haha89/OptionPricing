from option_vol.implied_vol_calculator import ImpliedVolCalculator

""" Display option_vol surface for TSLA listed options using marketwatch website"""

UNDERLYING = "TSLA"
RISK_FREE_RATE = 0.01
PATH_PNG = fr"C:\Users\E5420\PycharmProjects\OptionVol\images\vol_surface_{UNDERLYING}.png"

ImpliedVolCalculator(UNDERLYING, RISK_FREE_RATE, PATH_PNG).main()
