OPTION_ATTRIBUTES = ["name", "type", "underlying", "strike", "maturity", "price", "implied_vol",
                     "delta", "gamma", "theta", "vega", "rho"]


def display_options(elements):
    from prettytable import PrettyTable
    my_table = PrettyTable()
    attributes = _get_attributes(elements[0])
    my_table.field_names = attributes
    my_table.add_rows([_list_attributes(_, attributes) for _ in elements])
    return my_table


def _get_attributes(element):
    from option_vol.models import Put, Call
    if isinstance(element, (Call, Put)):
        return OPTION_ATTRIBUTES
    raise ValueError("Object doesnt have any mapping")


def _list_attributes(obj, attributes):
    return [round(e, 4) if isinstance(e := getattr(obj, o), float) else e for o in attributes]
