import dash
import dash_core_components as dcc
import dash_html_components as html
import json

app = dash.Dash(__name__)

serialized_components = """
[dbc.Row([
            dbc.Col(html.P("Hi! I'm C-4PM. How can I help you?", style={'text-align': 'left'},
                           className="from-them margin-b_one"), width=10),
            dbc.Col(html.P(["You can ask me multiple things, for example:",
                            html.Br(),
                            html.Br(),
                            html.Ul([
                                html.Li("Describe the process"),
                                html.Li("List the activities in the process"),
                                html.Li("Can you give me some conformant traces?"),
                                html.Li("Is it possible that ER Triage occurs before IV Liquids?"),
                                html.Li("In which cases ER Triage occurs right after ER Registration?")
                            ])],
                           style={'text-align': 'left'},
                           className="from-them margin-b_one"), width=10)]
        )]
"""


def parse_serialized_components(serialized_str):
    parsed_components = []

    try:
        components_data = json.loads(serialized_str)

        for component_data in components_data:
            component_type = getattr(dcc, component_data['type'])
            component_props = component_data['props']

            parsed_component = component_type(**component_props)
            parsed_components.append(parsed_component)

        return parsed_components

    except Exception as e:
        print(f"Error parsing serialized components: {str(e)}")
        return []


parsed_components = parse_serialized_components(serialized_components)

app.layout = html.Div(parsed_components)

if __name__ == '__main__':
    app.run_server(debug=True)
