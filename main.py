from dash import Dash, html
import dash_bootstrap_components as dbc
from callbacks import all_callbacks


def make_layout():
    return html.Div(children=[

        # Navbar
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="assets/bot.png", height="35px")),
                                dbc.Col(dbc.NavbarBrand("C-4PM", className="ms-2")),
                                dbc.Col()
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="https://plotly.com",
                        style={"textDecoration": "none"},
                    ),
                ]
            ),
            color="dark",
            dark=True,
            className="navbar-custom",
            fixed="top"
        ),

        dbc.Container([

            dbc.Modal([
                dbc.ModalHeader(
                    dbc.ModalTitle("Welcome to C-4PM"),
                    close_button=True),
                dbc.ModalBody([
                    html.H4("Demo usage ⚠️", className="alert-heading"),
                    html.P(
                        "As C-4PM is still in active development, for offering a stable experience during this "
                        "preliminary testing stages, the use of the tool is limited to the Sepsis use-case described "
                        "in the paper. "
                        "Both event log and process specification are given to the system by default, so the user can test "
                        "the proposed reasoning tasks in a controlled environment."
                    ),
                ]),
                dbc.ModalFooter([
                    html.P(
                        "We apologize in advance for the inconvenience.",
                    ), ])
            ], centered=True, is_open=True),

            dbc.Row([
                dbc.Col([

                    # Chat window
                    dbc.Row([
                        html.Div(id='conversation', className="imessage"),
                        # style={'height': '300px', 'overflow': 'scroll', 'flex-direction': 'column-reverse'},

                        # dcc.Loading(id="ls-loading-1", children=[html.Div(id="loading-output")],type="default"),

                        # Loading
                        # dbc.Row([
                        #     html.Br(),
                        #     dbc.Col(html.P(dls.Pulse(html.Div(id="loading-output", style={'text-align': 'left'}),
                        #                              width=35, color='#999999'), className='from-them margin-b_one'),
                        #             width=3),
                        #     html.Br(),
                        #     html.Br(),
                        # ]),
                    ]),

                ], width=12, lg=8)

            ], justify="center", className="conversation"),

            html.Br(),

        ], fluid=True, className="p0"),

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
                                        dbc.Spinner(html.Div(id="loading-output"), color="light",
                                                    size="sm"),
                                        id='send_button', type='submit', n_clicks=0, color="info")
                                    ], className="d-grid gap-2", width=2)
                            ])
                        ], width=12, lg=8)
                    ], justify="center")
                ])
            ], fluid=True, className="p0"),
        ], className="typing")

    ])


def init_app():
    dash_app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.COSMO],
        title="C-4PM",
        suppress_callback_exceptions=True
    )

    dash_app.layout = make_layout()
    all_callbacks(dash_app)
    return dash_app


if __name__ == '__main__':

    # endpoints = EndpointConfig("http://localhost:5055/webhook")
    # chat("models/20230522-122709-vivid-shore.tar.gz", endpoints="endpoints.yml")
    # rasa.run(model="models/20230522-122709-vivid-shore.tar.gz", endpoints="endpoints.yml")
    # clitest.chat("models/20230522-122709-vivid-shore.tar.gz", endpoints="endpoints.yml")

    app = init_app()
    app.run_server(debug=False, port=8080, dev_tools_hot_reload=False)
