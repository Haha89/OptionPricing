# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash
from dashboard.callbacks import assign_callbacks
from dashboard.layout import set_layout


def run_app():
    app = Dash(__name__)
    app.layout = set_layout(app)
    assign_callbacks(app)
    app.run_server(debug=True)


if __name__ == '__main__':
    run_app()
