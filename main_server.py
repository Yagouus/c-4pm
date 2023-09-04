import main
from dash import Dash
import dash_bootstrap_components as dbc
import config
from callbacks import all_callbacks


def init_dashboard(server):
    dash_app = Dash(
        server=server,
        url_base_pathname=config.url_base_pathname,
        external_stylesheets=[dbc.themes.COSMO],
        title="C-4PM"
    )

    dash_app.layout = main.make_layout()
    all_callbacks(dash_app)
    return dash_app.server
