import dash
from dash import html, dcc, Input, Output, State
import time

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Input(id='input-message', type='text', placeholder='Enter your message'),
        html.Button('Send', id='send-button'),
    ]),

    html.Div(id='display-sent-message', children=[
        html.Div('Sent Messages: ')
    ]),
    html.Div(id='display-received-message', children=[
        html.Div('Received Messages: ')
    ]),

    dcc.Store(id='store-messages', data={'sent': [], 'received': []}),
])

@app.callback(
    Output('store-messages', 'data'),
    [Input('send-button', 'n_clicks')],
    [State('input-message', 'value'),
     State('store-messages', 'data')]
)
def update_store(n_clicks, message, store_data):
    if n_clicks is None:
        return dash.no_update

    store_data['sent'].append(message)
    store_data['received'].append(message)  # You can update this based on the real received message
    return store_data

@app.callback(
    Output('display-sent-message', 'children'),
    [Input('store-messages', 'data')]
)
def update_sent_display(store_data):
    if not store_data['sent']:
        return dash.no_update

    sent_messages = [html.P(message, style={'text-align': 'right'}, className="from-me") for message in store_data['sent']]
    sent_messages.insert(0, html.Div(children='Sent Messages: '))
    return sent_messages

@app.callback(
    Output('display-received-message', 'children'),
    [Input('store-messages', 'data')],
    [State('display-received-message', 'children')],
    prevent_initial_call=True
)
def update_received_display(store_data, existing_messages):
    ctx = dash.callback_context
    if not ctx.triggered or not store_data['received']:
        return dash.no_update

    # Simulate a delay for received messages
    time.sleep(2)

    received_messages = [html.P(message, style={'text-align': 'left'}, className="from-them") for message in store_data['received']]
    received_messages.insert(0, html.Div(children='Received Messages: '))
    return received_messages

if __name__ == '__main__':
    app.run_server(debug=True)
