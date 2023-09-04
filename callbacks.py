import time
from pathlib import Path

import rasa_connector

from dash import Dash, html, Output, Input, State, dash_table
import dash_bootstrap_components as dbc

# init a list of the sessions conversation history
conv_hist = []


def all_callbacks(dash_app):

    # Initialize the conversational agent
    model_path = rasa_connector.get_latest_model(Path("models"))
    agent = rasa_connector.launch_bot(model_path, endpoints="endpoints.yml")

    @dash_app.callback(
        Output(component_id='conversation', component_property='children'),
        Output(component_id="loading-output", component_property="children"),
        Output(component_id='msg_input', component_property='value'),
        Output(component_id='send_button', component_property='disabled'),
        Input(component_id='send_button', component_property='n_clicks'),
        State(component_id='msg_input', component_property='value'))
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
                # dbc.Col(html.Img(src="assets/bot.png", style={'width': '40px'}), width=1),
                dbc.Col(html.P("Hi! I'm C-4PM. How can I help you?", style={'text-align': 'left'},
                               className="from-them margin-b_one"), width=10),
                dbc.Col(html.P(["You can ask me multiple things, for example:",
                                html.Br(),
                                html.Br(),
                                html.Ul([
                                    html.Li("Describe the process"),
                                    html.Li("List the activities in the process"),
                                    html.Li("Does the model accept any behavior?"),
                                    html.Li("Can you give me some conformant traces?"),
                                    html.Li("Is it possible that ER Triage occurs before IV Liquids?"),
                                    html.Li("Can activity IV Antibiotics be performed before activity Admission NC?"),
                                    html.Li("In which cases ER Triage occurs right after ER Registration?"),
                                    html.Li("Will IV Antibiotics eventually happen twice?")
                                ])],
                               style={'text-align': 'left'},
                               className="from-them margin-b_one"), width=10)]
            )]
            conv_hist = rspd
            return conv_hist, html.Div('Send'), '', False

    # trigger bot response to user inputted message on submit button click
    @dash_app.callback(
        Output(component_id='conversation', component_property='children', allow_duplicate=True),
        Output(component_id="loading-output", component_property="children", allow_duplicate=True),
        Output(component_id='send_button', component_property='disabled', allow_duplicate=True),
        Input(component_id='send_button', component_property='n_clicks'),
        State(component_id='msg_input', component_property='value'),
        prevent_initial_call=True)
    def update_conversation(click, text):
        global conv_hist

        # dont update on app load
        if click > 0 and text != '':

            print(text)

            # call bot with user inputted text
            # response = [{"text": "Response"}]
            response = rasa_connector.talk(agent, text)

            # user message aligned left
            # rcvd = [html.P(text, style={'text-align': 'right'})]

            rspd = []

            print(response)

            for idx, r in enumerate(response):

                for response_type, value in r.items():

                    if response_type == "text":

                        if idx == len(response) - 1:
                            rspd.append(dbc.Row([
                                # dbc.Col(html.Img(src="assets/bot.png", style={'width': '40px'}),
                                #        width=1),
                                dbc.Col(html.P(value, style={'text-align': 'left'}, className="from-them margin-b_one"),
                                        width=10)]
                            ))
                        else:
                            rspd.append(dbc.Row([
                                # dbc.Col(html.P(style={'width': '40px'}),
                                #       width=1),
                                dbc.Col(html.P(value, style={'text-align': 'left'}, className="from-them margin-b_one"),
                                        width=10)]
                            ))

                    # if response_type == "image":
                    #    image = Image(url=value)
                    #   display(image)

            agent_convo = rspd[::-1]

            # append interaction to conversation history
            conv_hist = agent_convo + conv_hist

            time.sleep(1)
            return conv_hist, html.Div('Send'), False

        else:
            return '', html.Div('Send'), False

    # @app.callback(
    #     Output('send_button', 'disabled'),
    #     Input('msg_input', 'value'))
    # def set_button_enabled_state(on_off):
    #     if on_off != '':
    #         return False
    #     else:
    #         return True
