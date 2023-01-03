import pandas as pd
from datetime import datetime

BASE_URL = "https://bigcharts.marketwatch.com/quickchart/options.asp?symb="
INDEX_TABLE = 2


class Scrapping:

    def __init__(self):
        self.mat = ""

    def parse_option(self, underlying):
        """
        Retrieves listed options for an underlying with their Strike and ask price
        :param underlying: string, name of the underlying
        :return: a pandas DataFrame containing all options found in the website:

        | option_type | strike | maturity     | price |
        -------------------------------------------
        |      C      |  50    |  01/01/2022  |   1   |
        |      P      |  50    |  01/01/2022  |   0   |

        """

        found_options = []
        options = pd.read_html(f"{BASE_URL}{underlying}")[INDEX_TABLE]
        options = options[[c for c in options.columns if options[c].isin(["Ask", "StrikePrice"]).any()]]
        options.columns = ["call_ask", "strike", "put_ask"]

        def read_row(row):
            if "Expires " in str(row.call_ask):
                self.mat = datetime.strptime(row.call_ask.replace("Expires ", ""), "%B %d, %Y").date()

            elif is_float(row.call_ask):
                found_options.append(("C", float(row.strike), self.mat, float(row.call_ask)))
                found_options.append(("P", float(row.strike), self.mat, float(row.put_ask)))

        options.apply(lambda r: read_row(r), axis=1)
        return pd.DataFrame(found_options, columns=["option_type", "strike", "maturity", "price"])


def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except (ValueError, TypeError):
        return False
