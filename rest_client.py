import dash
from dash import dcc, html, Input, Output, State
import requests
import uuid

app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div([
    html.H1("Rasa Bot"),
    dcc.Store(id='session-id', storage_type='session'),  # Store for session ID
    dcc.Store(id='conversation-history', data={'messages': []}),  # Store for conversation history
    dcc.Textarea(
        id='user-input',
        placeholder='Enter your message...',
        style={'width': '50%', 'height': 100},
    ),
    html.Button('Send', id='send-button'),
    html.Div(id='bot-response', children=[]),
    html.Div(id='client_identifier')
])


# Function to query Rasa
def query_rasa(text, session_id):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": session_id,
        "message": text
    }
    response = requests.post(url, json=payload)
    return response.json()


# Callback to initialize session ID
@app.callback(
    Output('session-id', 'data'),
    Output('client_identifier', 'children'),
    Input('send-button', 'n_clicks'),
    prevent_initial_call=True
)
def initialize_session(n_clicks):
    id = str(uuid.uuid4())
    return {'id': id}, id


# Callback for handling button click and updating conversation history
@app.callback(
    [Output('bot-response', 'children'),
     Output('conversation-history', 'data')],
    [Input('send-button', 'n_clicks')],
    [State('user-input', 'value'),
     State('session-id', 'data'),
     State('conversation-history', 'data')]
)
def send_to_bot(n_clicks, user_input, session_data, conversation_history):
    if n_clicks is None:
        return [], {'messages': []}

    # Retrieve or generate session ID
    session_id = session_data.get('id') if session_data else str(uuid.uuid4())

    # Query Rasa and get the response
    responses = query_rasa(user_input, session_id)
    response_texts = [res['text'] for res in responses if 'text' in res]

    # Update conversation history
    updated_messages = conversation_history['messages']
    updated_messages.append({'sender': 'User', 'message': user_input})
    updated_messages.extend([{'sender': 'Bot', 'message': res} for res in response_texts])

    # Create display elements
    display_elements = []
    for message in updated_messages:
        display_elements.append(html.P(f"{message['sender']}: {message['message']}"))

    return display_elements, {'messages': updated_messages}


if __name__ == '__main__':
    app.run_server(debug=True)
