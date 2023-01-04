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
        return self._query(underlying, "spots")

    def get_div_yield(self, underlying):
        return self._query(underlying, "div_yield")

    def get_listed_options(self, underlying):
        return self._query(underlying, "listed_options")

    def _query(self, underlying, shelf):
        """ Retrieves market data of 3 types: spots, div_yields and listed options. Results are cached for later use """
        content = getattr(self, shelf)
        if underlying not in content:
            match shelf:
                case "spots":
                    import yfinance as yf
                    val = yf.download(tickers=underlying, period='1d', interval='1d')["Adj Close"][0]
                case "div_yield":
                    val = 0  # TO BE DONE
                case "listed_options":
                    from option_vol.scrapping import Scrapping
                    val = Scrapping().parse_option(underlying=underlying)
                case _:
                    raise ValueError(f"Store {shelf} not found")
            content[underlying] = val
        return content[underlying]
