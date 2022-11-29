import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_mantine_components as dmc
import random
import base64


def footprint_card(name):
    # Random number 3-8
    footprint = round(random.randint(300, 800) * 0.0001, 4)
    # Random number 30-80
    footprint2 = round(random.randint(30, 80) * 0.0001, 4)

    if name == "The Marina Phuket Hotel ":
        footprint = 0.0187
        footprint2 = 0.035

    return dbc.Card([
        dbc.CardHeader("Guest Carbon Footprint", style={'font-size': '14px', 'font-weight': 'bold', 'color': 'white',
                                                        'background-color': '#3498DB', 'border-radius': '10px',
                                                        'margin': '10px', 'margin-right': '210px'}),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.P("Rooms Footprint", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"{footprint} MTCO₂e", className="card-text",
                               style={'font-size': '14px'}),
                    ], style={'text-align': 'right'})
                ]),
                dbc.Row([
                    dbc.Col([
                        html.P("Meetings Footprint", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"{footprint2} MTCO₂e", className="card-text",
                               style={'font-size': '14px'}),
                    ], style={'text-align': 'right'})
                ]),
                dbc.Row([
                    dbc.Col([
                        html.P("Total:", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"{round(footprint + footprint2, 4)} MTCO₂e", className="card-text",
                               style={'font-size': '14px'}),
                    ], style={'text-align': 'right'})
                ]),
            ], style={'padding': '10px'}
        ),
    ], style={'border': '5px', 'border-radius': '20px', 'border-color': 'black', 'margin': '10px'})


def hotel_card(name):
    # Random number 3-8
    footprint = round(random.randint(300, 800) * 0.0001, 4)
    # Random number 30-80
    footprint2 = round(random.randint(30, 80) * 0.0001, 4)

    return dbc.Card([
        dbc.CardHeader("Hotel Benchmark Results by Year",
                       style={'font-size': '14px', 'font-weight': 'bold', 'color': 'white',
                              'background-color': '#1ABC9C', 'border-radius': '10px',
                              'margin': '10px', 'margin-right': '140px'}),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.P("Energy Usage per SqM", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"{int(random.randint(200, 500))} kWh", className="card-text",
                               style={'font-size': '14px'}),
                    ], style={'text-align': 'right'})
                ]),
                dbc.Row([
                    dbc.Col([
                        html.P("Carbon emissions per SqM", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"{round(footprint * 0.8, 4)} MTCO₂e", className="card-text",
                               style={'font-size': '14px'}),
                    ], style={'text-align': 'right'})
                ]),
                dbc.Row([
                    dbc.Col([
                        html.P("Ranking by Location", className="card-title",
                               style={'font-size': '14px', 'font-weight': 'bold', 'margin-left': '0px'}),
                    ], style={'text-align': 'left'}),
                    dbc.Col([
                        html.P(f"{int(random.randint(1, 10))}th decile", className="card-text",
                               style={'font-size': '14px'}),
                    ], style={'text-align': 'right'})
                ]),
            ], style={'padding': '10px'}
        ),
    ], style={'border': '5px', 'border-radius': '20px', 'border-color': 'black', 'margin': '10px'})


def footprint_modal(name):
    with open('assets/Hotel_Carbon_Footprint_Report.pdf', 'rb') as pdf:
        pdf_data = base64.b64encode(pdf.read()).decode('utf-8')
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Carbon Footprint Report", style={'font-size': '18px'}),
                        close_button=True),
        dbc.ModalBody(
            html.Div([
                dcc.Loading(
                    dash.html.ObjectEl(data='data:application/pdf;base64,' + pdf_data,
                                       type='application/pdf',
                                       style={'width': '100%', 'height': '67vh'})
                )
            ], style={'padding': '10px', 'margin': '10px'})
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id=f"close-footprint-modal",
                className="ms-auto",
                n_clicks=0,
                style={"background-color": "#BDBEC8", "border": "none", "border-radius": "12px",
                       "box-shadow": "0px 3px 20px rgba(161, 183, 205, 0.2)"}
            )
        ),
    ],
        id=f"footprint-modal",
        scrollable=True,
        centered=True,
        is_open=False,
        size="xl"
    )


def benchmark_modal(name):
    with open('assets/Hotel_Energy_Report.pdf', 'rb') as pdf:
        pdf_data = base64.b64encode(pdf.read()).decode('utf-8')
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Hotel Benchmarking Results", style={'font-size': '18px'}),
                        close_button=True),
        dbc.ModalBody(
            html.Div([
                dcc.Loading(
                    dash.html.ObjectEl(data='data:application/pdf;base64,' + pdf_data,
                                       type='application/pdf',
                                       style={'width': '100%', 'height': '67vh'})
                )
            ], style={'margin': '10px'})
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
        size="xl"
    )


def filter_drawer():
    return dmc.Drawer(
        html.Div([
            html.H3("FILTERS", className='dropdown-labels',
                    style={'font-size': '18px', 'font-weight': 'bold',
                           'margin': '20px'}),
            dbc.Row([
                # Filters
                html.Label("Filter by Review Score", className='dropdown-labels'),
                html.Div([
                    dcc.RangeSlider(0, 10, id='price-range', value=[0, 10],
                                    tooltip={"placement": "bottom", "always_visible": True}),
                ], style={'margin-left': '10px'}),
                # Rating Filter
                html.Label("Filter by Stars", className='dropdown-labels'),
                html.Div([
                    dcc.RangeSlider(0, 5, id='review-range', value=[0, 5], step=0.5,
                                    tooltip={"placement": "bottom", "always_visible": True}),
                ], style={'margin-left': '10px'}),
                # Button apply filter
                html.Button(id='update-button', children="Apply Filter"),

            ], style={'background-color': '#fffff'}),
        ]),
        title="Drawer Example",
        id="drawer",
        padding="md",
        size=450,
        position="right",
    )


def generate_hotel_benchmark_report():
    with open('assets/Hotel_Energy_Report.pdf', 'rb') as pdf:
        pdf_data = base64.b64encode(pdf.read()).decode('utf-8')
    return html.Div([
        dcc.Loading(
            dash.html.ObjectEl(data='data:application/pdf;base64,' + pdf_data,
                               type='application/pdf',
                               style={'width': '100%', 'height': '67vh'})
        )
    ],
        className="card_body",
        style={'margin-left': '10px', 'margin-right': '30px'}
    )


def generate_alto_solution(i):
    package_name_dict = {
        1: ['Experience Package', 'Real-Time Operation'],
        2: ['Integration Package', 'IoT Integration'],
        3: ['Ultimate Package', 'AI Automation'],
    }

    package_color_dict = {
        1: '#BDC3C7',
        2: '#1ABC9C',
        3: '#3498DB',
    }

    package_description_dict = {
        1: 'Real-Time Operation',
        2: 'IoT Integration',
        3: 'AI Automation',
    }

    package_price_dict = {
        1: "Free trial 3 months 100 baht/room/month",
        2: "12,000 baht/room per month",
        3: "Free upgrade (benefit sharing model)",
    }

    package_results_dict = {
        1: ["Avoid 194,174 kgCO₂e", ""],
        2: ["Avoid 388,348 kgCO₂e", "Save 783,075 kWh"],
        3: ["Avoid 1,165,045 kgCO₂e", "Save 2,349,225 kWh"],
    }

    def add_column_name(i):
        if i == 1:
            return dbc.Row([
                dbc.Col([
                    html.H5("Package Name", className="card_title"),
                ], xs=2),
                dbc.Col([
                    html.H5("Description", className="card_title"),
                ], xs=4),
                dbc.Col([
                    html.H5("Investment", className="card_title", style={'text-align': 'left', 'margin-left': '5px'}),
                ], xs=2),
                dbc.Col([
                    html.H5("Guaranteed Results (First Year)", className="card_title"),
                ])
            ])

    return add_column_name(i), html.Div([
        dbc.Row([
            # Alto Package Plan Name
            dbc.Col([
                dbc.CardHeader(package_name_dict[i][0],
                               style={'font-size': '14px', 'font-weight': 'bold', 'color': 'white',
                                      'background-color': package_color_dict[i], 'border-radius': '10px'}),
                html.H3(package_name_dict[i][1],
                        style={'font-size': '15px', 'margin-top': '20px', 'margin-left': '10px'}),
            ], xs=2),
            # Icons
            dbc.Col([
                html.Img(src=f"assets/alto_plan_{i}.png",
                         style={'width': '400px', 'margin-bottom': '-12px', 'float': 'right'}),
            ], xs=4),
            # Investment cost
            dbc.Col([
                html.H3(package_price_dict[i],
                        style={'font-size': '14px', 'margin-top': '40px'}),
            ], xs=2),
            # Results
            dbc.Col([
                html.H3(package_results_dict[i][0],
                        style={'font-size': '14px', 'margin-top': '40px'}),
            ]),
            dbc.Col([
                html.H3(package_results_dict[i][1],
                        style={'font-size': '14px', 'margin-top': '40px'}),
            ])
        ])
    ], className="card_body",
        style={'margin-right': '30px'})
