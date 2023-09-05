from dash import Dash, html
import dash_bootstrap_components as dbc

import callbacks_store
from layout import make_layout


def init_app():
    dash_app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.COSMO],
        title="C-4PM",
        suppress_callback_exceptions=True
    )

    dash_app.layout = make_layout()
    callbacks_store.all_callbacks(dash_app)
    return dash_app


if __name__ == '__main__':
    app = init_app()
    app.run_server(debug=False, port=8080, dev_tools_hot_reload=False)
