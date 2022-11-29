import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import app
from utils.preprocess_utils import *
from utils.visualize_utils import *
from utils.dashboard_utils import *

server = app.server

# app_port = os.environ['APP_PORT']
app_port = '80'


def serve_layout() -> html.Div:
    return html.Div([
        dbc.Row([
            # Left column
            dbc.Col([
                html.Div([
                    # Header
                    dbc.Col([
                        html.Img(src="assets/altologo.png", style={'width': '50px', 'margin': '11px', 'float': 'left'}),
                        html.H1("Hotel Footprinting Tool")
                    ]),
                    # Description
                    html.P("Calculate the carbon footprint of your hotel stay and meeting in Phuket and \
                    benchmark hotel with Cornell Hotel Sustainability Benchmarking (CHSB) index using \
                    real-time hotel data supplied by TAT "),

                    # 1. Search Hotel
                    html.Label("1. PICK A HOTEL", className='dropdown-labels'),
                    dbc.Row([
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
                        html.Label("2. GET THE RESULTS", className='dropdown-labels'),
                        # Footprint report
                        html.Div(id='full-results', children=None,
                                 style={'margin': '10px', 'padding-right': '10px'}),
                        # See full results button
                        html.Div(id='full-results-button', children=None)
                    ]),
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
                ])
            ], xs=3),
            # Right column map
            dbc.Col([
                html.Div([
                    dcc.Loading(
                        dcc.Graph(id='mapbox')
                        , type="circle")
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="assets/all_logo.png",
                                     style={'width': '500px', 'margin': '0px', 'float': 'left'}),
                        ])
                    ])
                ], id='footer')
            ], xs=9)
        ]),
        html.Div(id='benchmark-results', style={'display': 'none'})
    ])


app.layout = serve_layout()


@app.callback(
    [Output('search', 'options'),
     Output('mapbox', 'figure'),
     Output('full-results', 'children'),
     Output('benchmark-results', 'children'),
     Output('full-results-button', 'children')],
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
        footprint_report = None
        modal_report = None
        modal_button = None

    else:
        fig_map = build_map(dff, filter=True, name=name)
        footprint_report = footprint_card()
        modal_report = benchmark_modal()
        modal_button = html.Button(id='results-button', children="See Benchmark Results"),

    return dd_options, fig_map, footprint_report, modal_report, modal_button


@app.callback(
    Output("benchmark-modal", "is_open"),
    [Input("results-button", "n_clicks"), Input("close-benchmark-modal", "n_clicks")],
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


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=app_port)
