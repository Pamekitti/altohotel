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
            # Left column
            dbc.Col([
                html.Div([
                    # Description
                    html.P("Calculate the carbon footprint of your hotel stay and meeting in Phuket and \
                    benchmark hotel with Cornell Hotel Sustainability Benchmarking (CHSB) index using \
                    real-time hotel data supplied by TAT ",
                           style={'margin': '20px'}),

                    # 1. Search Hotel
                    html.Label("1. PICK A HOTEL", className='dropdown-labels'),
                    html.P('Select a specific hotel from the map or use the search bar',
                           style={'margin-bottom': '-10px'}),
                    dbc.Row([
                        dbc.Col([
                            html.Button(id='drawer-button', children="Filters"),
                        ], width=2),
                        dbc.Col([
                            html.Div([
                                dcc.Dropdown(
                                    id='search',
                                    placeholder='Select a hotel',
                                    searchable=True,
                                    optionHeight=20,
                                    style={'xoverflow': 'scroll', 'yoverflow': 'scroll'}
                                ),
                            ], style={'width': '100%', 'margin-left': '20px', 'margin': '10px',
                                      'xoverflow': 'scroll', 'yoverflow': 'scroll',
                                      'padding': '10px', 'float': 'left'}),
                        ]),
                    ]),

                    dbc.Row([
                        # 2. See Result
                        html.Label("2. GET THE RESULTS", className='dropdown-labels',
                                   style={'margin-bottom': '-10px'}),
                        # Footprint report
                        html.Div(id='footprint-summary', children=None,
                                 style={'margin': '10px', 'padding-right': '10px'}),
                        html.Div(id='footprint-button', children=None),

                        # Hotel Benchmark summary
                        html.Div(id='hotel-summary', children=None,
                                 style={'margin': '10px', 'padding-right': '10px'}),
                        html.Div(id='benchmark-button', children=None),

                    ]),
                    dbc.Row([

                    ], style={'background-color': '#fffff'}),
                ])
            ], xs=4),
            # Right column map
            dbc.Col([
                html.Div([
                    dcc.Graph(id='mapbox')
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="../assets/all_logo.png",
                                     style={'width': '500px', 'margin': '0px', 'float': 'left'}),
                        ])
                    ])
                ], id='footer')
            ], xs=8)
        ]),
        html.Div(id='footprint-results', style={'display': 'none'}),
        html.Div(id='benchmark-results', style={'display': 'none'}),
        filter_drawer(),
    ])


app.layout = serve_layout()


@app.callback(
    [Output('search', 'options'),
     Output('mapbox', 'figure'),
     Output('footprint-summary', 'children'),
     Output('hotel-summary', 'children'),
     Output('footprint-results', 'children'),
     Output('footprint-button', 'children'),
     Output('benchmark-results', 'children'),
     Output('benchmark-button', 'children')],
    [State('price-range', 'value'),
     State('review-range', 'value'),
     Input('search', 'value'),
     Input('update-button', 'n_clicks')]
)
def update_output(price_range, review_range, name, filter_clicks):
    df = get_hotel_data('assets/data_hotel_01.csv')
    df_dict, dd_options, dd_defaults = df_to_dd_options(df)
    dff = df.copy()
    if filter_clicks:
        dff = df[(df['review_score'] >= price_range[0]) & (df['review_score'] <= price_range[1]) &
                 (df['rating'] >= review_range[0]) & (df['rating'] <= review_range[1])]

    if name is None:
        fig_map = build_map(dff)

        footprint_summary = None
        guest_modal_report = None
        footprint_button = None

        hotel_summary = None
        hotel_modal_report = None
        hotel_modal_button = None

    else:
        fig_map = build_map(dff, filter=True, name=name)

        footprint_summary = footprint_card(name)
        guest_modal_report = footprint_modal(name)
        footprint_button = html.Button(id='guest-button', children="Get Footprint Report")

        hotel_summary = hotel_card(name)
        hotel_modal_report = benchmark_modal(name)
        hotel_modal_button = html.Button(id='hotel-button', children="See Benchmark Results")

    return [dd_options, fig_map, footprint_summary, hotel_summary, guest_modal_report, footprint_button,
            hotel_modal_report, hotel_modal_button]


# Callback for Carbon footprint modal
@app.callback(
    Output("footprint-modal", "is_open"),
    [Input("guest-button", "n_clicks"), Input("close-footprint-modal", "n_clicks")],
    [State("footprint-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """ Toggle the info modal.
    Args:
        n1: number of clicks on the info button.
        n2: number of clicks on the close button.
        is_open: boolean value indicating whether the modal is open or not.
    Returns:
        boolean value indicating whether the modal is open or not.
    """
    if n1 or n2:
        return not is_open
    return is_open


# Callback for Benchmark results modal
@app.callback(
    Output("benchmark-modal", "is_open"),
    [Input("hotel-button", "n_clicks"), Input("close-benchmark-modal", "n_clicks")],
    [State("benchmark-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """ Toggle the info modal.
    Args:
        n1: number of clicks on the info button.
        n2: number of clicks on the close button.
        is_open: boolean value indicating whether the modal is open or not.
    Returns:
        boolean value indicating whether the modal is open or not.
    """
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('search', 'value'),
    [Input('mapbox', 'clickData')]
)
def crossfiltering_update_search(hoverData):
    if hoverData is None:
        return None
    else:
        return hoverData['points'][0]['text']


@app.callback(
    Output("drawer", "opened"),
    Input("drawer-button", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_demo(n_clicks):
    return True
