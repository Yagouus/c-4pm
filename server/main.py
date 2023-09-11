import layout
from dash import Dash
import dash_bootstrap_components as dbc
from server import config
import callbacks_store


def init_dashboard(server):
    dash_app = Dash(
        server=server,
        url_base_pathname=config.url_base_pathname,
        external_stylesheets=[dbc.themes.COSMO],
        assets_folder="../assets",
        title="C-4PM"
    )

    dash_app.layout = layout.make_layout()
    callbacks_store.all_callbacks(dash_app=dash_app, url="http://172.16.240.98:5005/webhooks/rest/webhoo")
    return dash_app.server
