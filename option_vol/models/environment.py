import yfinance as yf


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance


class Environment(Singleton):
    spots, div_yield = {}, {}
    risk_free_rate = 0
    listed_options = {}

    def get_spot(self, underlying):
        if underlying not in self.spots:
            self.spots[underlying] = yf.download(tickers=underlying, period='1d', interval='1d')["Adj Close"][0]
        return self.spots[underlying]

    def get_div_yield(self, underlying):
        if underlying not in self.div_yield:
            self.div_yield[underlying] = 0
        return self.div_yield[underlying]

    def get_listed_options(self, underlying):
        if underlying not in self.listed_options:
            from option_vol.scrapping import Scrapping
            self.listed_options[underlying] = Scrapping().parse_option(underlying=underlying)
        return self.listed_options[underlying]
