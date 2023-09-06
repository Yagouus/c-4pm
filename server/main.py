import layout
from dash import Dash
import dash_bootstrap_components as dbc
from server import config
from callbacks_store_server import all_callbacks


def init_dashboard(server):
    dash_app = Dash(
        server=server,
        url_base_pathname=config.url_base_pathname,
        external_stylesheets=[dbc.themes.COSMO],
        assets_folder="../assets",
        title="C-4PM"
    )

    dash_app.layout = layout.make_layout()
    all_callbacks(dash_app)
    return dash_app.server
