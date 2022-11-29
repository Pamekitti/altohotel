import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import app
from utils.preprocess_utils import *
from utils.visualize_utils import *
from utils.dashboard_utils import *


def serve_layout() -> html.Div:
    return html.Div([
        html.Img(src=app.get_asset_url('plans.png'),
                 style={'width': '60%', 'height': '60%',
                        'margin-left': '20%', 'margin-top': '5%'}),
    ])


app.layout = serve_layout
