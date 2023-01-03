from pydantic import BaseModel
import yfinance as yf


class Environment(BaseModel):
    risk_free_rate: float
    spots = {}

    def get_spot(self, underlying):
        if underlying not in self.spots:
            self.spots[underlying] = yf.download(tickers=underlying, period='1d', interval='1d')["Adj Close"][0]
        return self.spots[underlying]
