from typing import List

import pandas as pd

from option_vol.models import BaseOption


class Plotting:
    @staticmethod
    def display_surfaces(options: List[BaseOption], elements: List[str], path_png: str):
        """ This functions generate two charts of 3d surface (one for Calls, one for Puts) of the evolution of
         element for multiple strikes and maturity dates

        :param options List of BaseOptions priced
        :param elements List of str, greeks to display
        """
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        df = pd.DataFrame(
            [(o.type, o.strike, o.maturity) + tuple(map(lambda e: o.__getattribute__(e), elements)) for o in options],
            columns=["type", "strike", "maturity"] + elements)

        option_types = df.type.unique()
        nb_rows, nb_cols = len(elements), len(option_types)
        fig = make_subplots(rows=nb_rows, cols=nb_cols, specs=[[{"type": "surface"}] * nb_cols] * nb_rows)
        labels = []
        for c, option_type in enumerate(option_types):
            f_options = df[df.type == option_type]
            for r, element in enumerate(elements):
                pivot = f_options.pivot_table(index="strike", values=element, columns="maturity", aggfunc='first')
                fig.add_trace(go.Surface(x=pivot.columns, y=pivot.index, z=pivot.values, showscale=False),
                              row=r + 1, col=c + 1)
                labels.append(dict(xaxis_title='Maturity', yaxis_title='Strike', zaxis_title=element))

        scenes = [f"scene{i if i > 1 else ''}" for i in range(1, nb_rows * nb_cols + 1)]

        fig.update_layout(
            template="plotly_dark",
            margin=dict(r=10, t=25, b=40, l=60),
            annotations=[dict(text="Source: marketwatch", showarrow=False)],
            width=1500, height=1000, **dict(zip(scenes, labels))
        )
        if path_png:
            fig.write_image(path_png + f"/surface_{'-'.join(elements)}_{options[0].underlying}.png")
        fig.show()
