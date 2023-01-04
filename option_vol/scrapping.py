from datetime import datetime
from typing import List

import pandas as pd

from option_vol.models import Call, Put, BaseOption

BASE_URL = "https://bigcharts.marketwatch.com/quickchart/options.asp?symb="
INDEX_TABLE = 2


class Scrapping:

    def __init__(self):
        self.mat = datetime.today().date()

    def parse_option(self, underlying) -> List[BaseOption]:
        """
        Retrieves listed options for an underlying with their Strike and ask price
        :param underlying: string, name of the underlying
        :return: a list of BaseOption
        """

        found_options = []
        print("Parsing html from marketwatch")
        options = pd.read_html(f"{BASE_URL}{underlying}")[INDEX_TABLE]
        options = options[[c for c in options.columns if options[c].isin(["Ask", "StrikePrice"]).any()]]
        options.columns = ["call_ask", "strike", "put_ask"]

        def read_row(row):
            if "Expires " in str(row.call_ask):
                self.mat = datetime.strptime(row.call_ask.replace("Expires ", ""), "%B %d, %Y").date()

            elif is_float(row.call_ask):
                found_options.append(Call(float(row.strike), self.mat, underlying, float(row.call_ask)))
                found_options.append(Put(float(row.strike), self.mat, underlying, float(row.put_ask)))

        options.apply(lambda r: read_row(r), axis=1)
        return found_options


def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except (ValueError, TypeError):
        return False
