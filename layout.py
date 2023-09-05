from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def make_layout():
    return html.Div(children=[

        # Navbar
        dbc.Navbar(
            dbc.Container([
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/bot.png", height="35px")),
                        dbc.Col(dbc.NavbarBrand("C-4PM", className="ms-2")),
                    ], align="center", className="g-0")
            ]), color="dark", dark=True, className="navbar-custom", fixed="top"
        ),

        dbc.Container([

            dbc.Modal([
                dbc.ModalHeader(
                    dbc.ModalTitle("Welcome to C-4PM"), close_button=True),
                dbc.ModalBody([
                    html.H4("Demo usage ⚠️", className="alert-heading"),
                    html.P("As C-4PM is still in active development, for offering a stable experience during this "
                           "preliminary testing stages, the use of the tool is limited to the Sepsis"
                           " use-case described in the paper. "
                           "Both event log and process specification are given to the system by default,"
                           " so the user can test the proposed reasoning tasks in a controlled environment."
                           " IMPORTANT! There is no parallelization of C-4PM for multiple users implemented yet, "
                           "so we ask you for patience if you experience some delay between your question"
                           " and receiving and answer."),
                ]),
                dbc.ModalFooter([html.P("We apologize in advance for the inconvenience.")])
            ], centered=True, is_open=True),

            # Main conversation window
            dbc.Row([
                dbc.Col([dbc.Row([html.Div(id='conversation', className="imessage")])], width=12, lg=8)
            ], justify="center", className="conversation"),

            html.Br(),

        ], fluid=True, className="p0"),

        # Typing bar
        html.Div([
            dbc.Container([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col(
                                    [dbc.Input(id='msg_input', value='', type='text', placeholder="Say something...",
                                               debounce=True)
                                     ], width=9),
                                dbc.Col(
                                    [dbc.Button(
                                        dbc.Spinner(html.Div([html.Div("Send")], id="loading-output"), color="light",
                                                    size="sm"),
                                        id='send_button', type='submit', n_clicks=0, color="info")
                                    ], className="d-grid gap-2", width=2)
                            ])
                        ], width=12, lg=8)
                    ], justify="center")
                ])
            ], fluid=True, className="p0"),
        ], className="typing"),

        # Create a storage for the conversation
        dcc.Store(id='conversation-store', data={'history': []}),

    ])
