import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import app
from utils.preprocess_utils import *
from utils.visualize_utils import *
from utils.dashboard_utils import *


def serve_layout() -> html.Div:
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H3("Benchmark Your Hotel",
                        style={'margin': '20px 20px 0px 170px', 'font-size': '20px', 'font-weight': 'bold'}),
                html.Div([
                    dbc.Input(placeholder="Full Name", type="text", id="input-1-state"),
                    dbc.Input(placeholder="Email", type="email", id="input-2-state"),
                    dbc.Input(placeholder="Phone Number", type="number", id="input-3-state"),
                    dbc.Input(placeholder="Hotel Name", type="text", id="input-4-state"),
                    dbc.Select(placeholder="Country", id="select-5-state", options=[
                        {"label": "Thailand", "value": "Thailand"},
                        {"label": "Malaysia", "value": "Malaysia"},
                        {"label": "Singapore", "value": "Singapore"},
                        {"label": "Indonesia", "value": "Indonesia"},
                        {"label": "Vietnam", "value": "Vietnam"},
                        {"label": "Country", "value": "Country", "disabled": True},
                    ]),
                    dbc.Input(placeholder="Energy Usage Per Year (kWh)", type="number", id="input-6-state"),
                    dbc.Input(placeholder="Number of Guest Rooms", type="number", id="input-7-state"),
                    dbc.Input(placeholder="Average Percentage of Room Occupancy",
                              type="number", id="input-8-state", min=0, max=100, step=1),

                    dbc.Button("Benchmark", id="custom-benchmark-button", n_clicks=0),
                    ], className="card_body")
            ], xs=5),
            dbc.Col([
                html.H3("Hotel Benchmark Report",
                        style={'margin': '20px 20px 0px 260px', 'font-size': '20px', 'font-weight': 'bold'}),
                html.Div(children=[],
                    id='custom-benchmark-summary')
                ]),

        ]),
        html.H3("Our Solution Benchmark",
                style={'margin': '40px 20px 0px 550px', 'font-size': '20px', 'font-weight': 'bold'}),
        html.Div(id='alto-solution-1'),
        html.Div(id='alto-solution-2'),
        html.Div(id='alto-solution-3'),
        dbc.Button("Contact Us", id="contact-us-button", href="https://www.altotech.net/"),
    ])


app.layout = serve_layout


@app.callback(
    [Output("custom-benchmark-summary", "children"),
     Output("alto-solution-1", "children"),
     Output("alto-solution-2", "children"),
     Output("alto-solution-3", "children")],
    Input("custom-benchmark-button", "n_clicks")
)
def generate_report(n_clicks):
    if n_clicks > 0:
        return generate_hotel_benchmark_report(), generate_alto_solution(1), generate_alto_solution(2), generate_alto_solution(3)
    else:
        return None, None, None, None

