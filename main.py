import time

import clitest

import glob

from dash import Dash, dcc, html, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls

# Just to reduce TF logging
import os
import warnings
import logging

# Configuration fof the logger
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('werkzeug').setLevel(logging.ERROR)
warnings.simplefilter(action='ignore', category=FutureWarning)

# init app and add stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# define the model the chatbot will be using
#model_path = "models/20230522-122709-vivid-shore.tar.gz"
model_path = "models/20230613-222831-right-code.tar.gz"

# init the conversational agent
agent = clitest.launch_bot(model_path, endpoints="endpoints.yml")

# init a list of the sessions conversation history
conv_hist = []

# app ui
app.layout = dbc.Container(children=[

    # Title
    html.Br(),
    dbc.Row(dbc.Col(html.Div(html.H1('Welcome to C-4PM')))),
    dbc.Row(dbc.Col(html.Div("""C-4PM: Conversational Interface 4 (Declarative) Process Mining."""))),
    html.Br(),

    # Upload file div, do not allow multiple files
    dcc.Upload(
        id='upload-data',
        className='div_hover',
        children=html.Div([html.B('Drag'), ' and ', html.B('Drop'), ' or ', html.A(html.B('Select an Event Log'))]),
        multiple=True
    ),

    html.Br(),
    dbc.Row(dbc.Col(html.Div(html.H3("Let's chat!")))),

    dbc.Row([
        dbc.Col([

            # Chat window
            dbc.Row([
                html.Div(id='conversation', className="imessage"),
                # style={'height': '300px', 'overflow': 'scroll', 'flex-direction': 'column-reverse'},

                # Loading
                dbc.Row([
                    html.Br(),
                    dbc.Col(html.P(dls.Pulse(html.Div(id="loading-output", style={'text-align': 'left'}),
                                             width=35, color='#999999'), className='from-them margin-b_one'), width=3),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                ]),
            ]),

            dbc.Row([
                # Message window and button
                dbc.Form([
                    dbc.Row([
                        dbc.Col(
                            [dbc.Input(id='msg_input', value='', type='text', placeholder="Say something...",
                                       debounce=True)
                             ], width=10),
                        dbc.Col(
                            [dbc.Button('Send', id='send_button', type='submit', n_clicks=0, color="primary")
                             ], className="d-grid gap-2", width=2)
                    ])
                ])
            ])

        ], width=8)

    ], justify="center"),

])


# trigger bot response to user inputted message on submit button click
@app.callback(
    Output(component_id='conversation', component_property='children'),
    Output(component_id="loading-output", component_property="children"),
    Output(component_id='msg_input', component_property='value'),
    Output(component_id='send_button', component_property='disabled'),
    Input(component_id='send_button', component_property='n_clicks'),
    State(component_id='msg_input', component_property='value'))
# function to add new user interaction to conversation history
def update_from(click, text):
    global conv_hist

    # dont update on app load
    if click > 0 and text != '':

        # user message aligned left
        rcvd = [html.P(text, style={'text-align': 'right'}, className="from-me")]

        conv_hist = rcvd + conv_hist

        return conv_hist, html.Div(), '', True

    else:
        time.sleep(2)
        rspd = [dbc.Row([
            dbc.Col(html.Img(src="assets/bot.png", style={'width': '40px'}), width=1),
            dbc.Col(html.P("Hi! I'm C-4PM. How can I help you?", style={'text-align': 'left'},
                           className="from-them margin-b_one"), width=10)]
        )]
        conv_hist = rspd + conv_hist
        return conv_hist, html.Div(), '', False


# trigger bot response to user inputted message on submit button click
@app.callback(
    Output(component_id='conversation', component_property='children', allow_duplicate=True),
    Output(component_id="loading-output", component_property="children", allow_duplicate=True),
    Output(component_id='send_button', component_property='disabled', allow_duplicate=True),
    Input(component_id='send_button', component_property='n_clicks'),
    State(component_id='msg_input', component_property='value'),
    prevent_initial_call=True)
# function to add new bot interaction to conversation history
def update_conversation(click, text):
    global conv_hist

    # dont update on app load
    if click > 0 and text != '':

        print(text)

        # call bot with user inputted text
        # response = [{"text": "Response"}]
        response = clitest.talk(agent, text)

        # user message aligned left
        # rcvd = [html.P(text, style={'text-align': 'right'})]

        rspd = []

        print(response)

        for idx, r in enumerate(response):

            for response_type, value in r.items():

                if response_type == "text":

                    if idx == len(response) - 1:
                        rspd.append(dbc.Row([
                            dbc.Col(html.Img(src="assets/bot.png", style={'width': '40px'}),
                                    width=1),
                            dbc.Col(html.P(value, style={'text-align': 'left'}, className="from-them margin-b_one"),
                                    width=10)]
                        ))
                    else:
                        rspd.append(dbc.Row([
                            dbc.Col(html.P(style={'width': '40px'}),
                                    width=1),
                            dbc.Col(html.P(value, style={'text-align': 'left'}, className="from-them margin-b_one"),
                                    width=10)]
                        ))

                # if response_type == "image":
                #    image = Image(url=value)
                #   display(image)

        agent_convo = rspd[::-1]

        # append interaction to conversation history
        conv_hist = agent_convo + conv_hist

        time.sleep(2)
        return conv_hist, html.Div(), False

    else:
        return '', html.Div(), False


# @app.callback(
#     Output('send_button', 'disabled'),
#     Input('msg_input', 'value'))
# def set_button_enabled_state(on_off):
#     if on_off != '':
#         return False
#     else:
#         return True


if __name__ == '__main__':
    # endpoints = EndpointConfig("http://localhost:5055/webhook")
    # chat("models/20230522-122709-vivid-shore.tar.gz", endpoints="endpoints.yml")
    # rasa.run(model="models/20230522-122709-vivid-shore.tar.gz", endpoints="endpoints.yml")

    # clitest.chat("models/20230522-122709-vivid-shore.tar.gz", endpoints="endpoints.yml")

    app.run_server(debug=False, port=8080, dev_tools_hot_reload=False)
