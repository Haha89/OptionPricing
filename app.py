import os

from dash import Dash

from dashboard.callbacks import assign_callbacks
from dashboard.layout import set_layout


def run_app():
    app = Dash(__name__, assets_folder=os.getcwd() + '/dashboard/assets')
    app.layout = set_layout(app)
    assign_callbacks(app)
    app.run_server(host='0.0.0.0')


if __name__ == '__main__':
    run_app()
