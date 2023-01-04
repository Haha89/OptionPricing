from typing import List

import pandas as pd

from option_vol.models import BaseOption


class Plotting:
    @staticmethod
    def display_surfaces(options: List[BaseOption], element: str, path_png: str):
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        df = pd.DataFrame([(o.__class__.__name__, o.strike, o.maturity, o.__getattribute__(element)) for o in options],
                          columns=["type", "strike", "maturity", element])

        option_types = df.type.unique()
        fig = make_subplots(cols=len(option_types), specs=[[{"type": "surface"}] * len(option_types)])
        labels = dict(xaxis_title='Maturity', yaxis_title='Strike', zaxis_title='Impl. Vol')
        for i, option_type in enumerate(option_types):
            f_options = df[df.type == option_type]
            f_options = f_options.pivot_table(index="strike", values=element, columns="maturity", aggfunc='first')
            fig.add_trace(go.Surface(x=f_options.columns, y=f_options.index, z=f_options.values, showscale=False),
                          row=1, col=i + 1)

        fig.update_layout(
            template="plotly_dark",
            margin=dict(r=10, t=25, b=40, l=60),
            annotations=[dict(text="Source: marketwatch", showarrow=False)],
            scene=labels,
            scene2=labels,
            width=1500, height=1000
        )
        if path_png:
            fig.write_image(path_png)
        fig.show()
