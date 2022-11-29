import dash_bootstrap_components as dbc
from dash import dcc, html
import random


def footprint_card():
    # Random number 3-8
    footprint = int(random.randint(300, 800))
    # Random number 30-80
    footprint2 = int(random.randint(30, 80))
    return dbc.Card([
        dbc.CardHeader("Hotel Name", style={'font-size': '14px', 'font-weight': 'bold', 'color': 'white',
                                            'background-color': 'black'}),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.P("Rooms Footprint", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                        ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"0.0{footprint} MTCO₂e", className="card-text",
                               style={'font-size': '14px', 'font-weight': 'bold'}),
                        ], style={'text-align': 'right'})
                    ]),
                dbc.Row([
                    dbc.Col([
                        html.P("Meetings Footprint", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"0.00{footprint2} MTCO₂e", className="card-text",
                               style={'font-size': '14px', 'font-weight': 'bold'}),
                    ], style={'text-align': 'right'})
                ]),
                dbc.Row([
                    dbc.Col([
                        html.P("Total:", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"0.0{footprint+footprint2} MTCO₂e", className="card-text",
                               style={'font-size': '14px', 'font-weight': 'bold'}),
                    ], style={'text-align': 'right'})
                ]),
            ], style={'border': '1px solid black', 'padding': '10px'}
        ),
    ], style={'border': '5px', 'border-radius': '20px', 'border-color': 'black', 'margin': '10px'})


def benchmark_modal():
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Full Hotel Benchmarking Results", style={'font-size': '18px'}), close_button=True),
        dbc.ModalBody(
            html.Div([
                html.Img(src="assets/demo_hotel.png", style={'width': '100%', 'margin': '0px', 'float': 'left'}),
            ], style={'padding': '10px', 'margin': '10px'})
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id=f"close-benchmark-modal",
                className="ms-auto",
                n_clicks=0,
                style={"background-color": "#BDBEC8", "border": "none", "border-radius": "12px",
                       "box-shadow": "0px 3px 20px rgba(161, 183, 205, 0.2)"}
            )
        ),
    ],
        id=f"benchmark-modal",
        scrollable=True,
        centered=True,
        is_open=False,
        size="l"
    )
