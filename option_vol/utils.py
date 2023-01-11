from typing import List

import pandas as pd
from prettytable import PrettyTable

OPTION_ATTRIBUTES = ["name", "type", "underlying", "strike", "maturity", "price", "implied_vol",
                     "delta", "gamma", "theta", "vega", "rho"]

YAHOO_MAPPING = {"SPX": "^GSPC"}


def display_options(elements: List) -> PrettyTable:
    """ Format a list of objects as a table in the console. Headers are based on elements content class """
    my_table = PrettyTable()
    attributes = _get_attributes(elements[0])
    my_table.field_names = attributes
    my_table.add_rows([_list_attributes(_, attributes) for _ in elements])
    return my_table


def options_to_df(elements: List, decimals=4) -> pd.DataFrame:
    return pd.DataFrame([e.__dict__ for e in elements]).round(decimals)


def _get_attributes(element):
    from option_vol.models import Put, Call
    if isinstance(element, (Call, Put)):
        return OPTION_ATTRIBUTES
    raise ValueError("Object doesnt have any mapping")


def _list_attributes(obj, attributes) -> List:
    return [round(e, 4) if is_float(e := obj.__getattribute__(o)) else e for o in attributes]


def to_title(title: str) -> str:
    return title.replace("_", " ").title()


def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except (ValueError, TypeError):
        return False
