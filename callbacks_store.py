import time
import uuid

import dash
import requests
from dash import html, Output, Input, State
import dash_bootstrap_components as dbc


def query_rasa(text, session_id, url="http://localhost:5005/webhooks/rest/webhook"):
    payload = {
        "sender": session_id,
        "message": text
    }
    response = requests.post(url, json=payload)
    return response.json()


def all_callbacks(dash_app, url="http://localhost:5005/webhooks/rest/webhook"):
    @dash_app.callback(
        Output('session-id', 'data'),
        Output('client_identifier', 'children'),
        [Input('init', 'children')],
    )
    def initialize_session(_):
        identifier = str(uuid.uuid4())
        print(identifier)
        return {'id': identifier}, str(identifier)


    @dash_app.callback(
        [Output('conversation', 'children'),
         Output('loading-output', 'children'),
         Output('msg_input', 'value'),
         Output('send_button', 'disabled'),
         Output('conversation-store', 'data')],
        [Input('send_button', 'n_clicks')],
        [State('msg_input', 'value'),
         State('conversation-store', 'data')]
    )
    def update_from(n_clicks, text, store_data):

        if n_clicks is None or n_clicks < 1:
            store_data['history'] = [dbc.Row([
                dbc.Col(html.P("Hi! I'm C-4PM. How can I help you?", style={'text-align': 'left'},
                               className="from-them margin-b_one"), width=10),
                dbc.Col(html.P(["You can ask me multiple things, for example:", html.Br(), html.Br(),
                                html.Ul([
                                    (html.B("Process Description")),
                                    html.Li(html.I("Describe the process")),
                                    html.Li(html.I("Explain me the process")),
                                    html.Br(),
                                    (html.B("Consulting the activities in the process")),
                                    html.Li(html.I("List the activities in the process")),
                                    html.Li(html.I("Which activities are found in the process?")),
                                    html.Br(),
                                    (html.B("Consistency checking")),
                                    html.Li(html.I("Does the model accept any behavior?")),
                                    html.Li(html.I("Is the process specification satisfiable?")),
                                    html.Br(),
                                    (html.B("Search for traces (from the log) that conform (or not) to the model")),
                                    html.Li(html.I("Can you give me some conformant traces?")),
                                    html.Li(html.I("What are the cases that conform to the model?")),
                                    html.Li(html.I("How many traces don't conform to the specification?")),
                                    html.Br(),
                                    (html.B("Consistency checking with custom LTL")),
                                    html.Li(html.I("Is it possible that ER Triage occurs before IV Liquid?")),
                                    html.Li(html.I("Can activity IV Antibiotics be performed before activity Admission NC?")),
                                    html.Li(html.I("Is it possible that activity ERTriage occurs immediately after activity AdmissionNC is performed?")),
                                    html.Br(),
                                    (html.B("Conformance checking with custom LTL")),
                                    html.Li(html.I("In which cases ER Triage occurs right after ER Registration?")),
                                    html.Li(html.I("Will IV Antibiotics eventually happen twice?")),
                                    html.Li(html.I("Give me all cases in which activity ERTriage occurs immediately after "
                                            "activity AdmissionNC is performed"))
                                ])],
                               style={'text-align': 'left'}, className="from-them margin-b_one"), width=10)]
            )]

            return store_data['history'], dash.no_update, dash.no_update, False, store_data

        elif text == '':
            return store_data['history'], dash.no_update, dash.no_update, False, store_data

        # user message aligned right
        rcvd = [html.P(text, style={'text-align': 'right'}, className="from-me")]
        store_data['history'] = rcvd + store_data['history']

        return store_data['history'], html.Div(), '', True, store_data

    @dash_app.callback(
        [Output('conversation', 'children', allow_duplicate=True),
         Output('loading-output', 'children', allow_duplicate=True),
         Output('send_button', 'disabled', allow_duplicate=True),
         Output('conversation-store', 'data', allow_duplicate=True)],
        [Input('send_button', 'n_clicks')],
        [State('msg_input', 'value'),
         State('session-id', 'data'),
         State('conversation-store', 'data')],
        prevent_initial_call=True
    )
    def update_conversation(click, text, session_data, store_data):

        if click is None or text == '':
            return dash.no_update, dash.no_update, False, dash.no_update

        time.sleep(0.5)

        session_id = session_data.get('id') if session_data else str(uuid.uuid4())

        # Query Rasa and get the response
        response = query_rasa(text, session_id)

        rspd = [
            dbc.Row([
                dbc.Col(
                    html.P(value, style={'text-align': 'left'}, className="from-them margin-b_one"),
                    width=10
                )
            ])
            for r in response for response_type, value in r.items() if response_type == "text"
        ]

        rcvd = [html.P(text, style={'text-align': 'right'}, className="from-me")]

        store_data['history'] = rspd[::-1] + rcvd + store_data.get('history', [])

        return store_data['history'], html.Div('Send'), False, store_data
