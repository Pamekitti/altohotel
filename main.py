from preprocessing.clean_data import clean_hotel_data
from preprocessing.feature_engineering import feature_engineer
from preprocessing.graphs import *
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly
import plotly.express as px

# import plotly.figure_factory as ff
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import seaborn as sns

new_data = False
if new_data:
    ds = pd.read_csv('csv_files/hotel_data_expedia.csv')
    df = clean_hotel_data(ds)
    df.to_csv('cleaned_hotel.csv')
else:
    df = pd.read_csv('csv_files/cleaned_hotel.csv')
    print(f'Date contains {df.shape[0]} rows of hotels in Bangkok')

df = feature_engineer(df)
train = df[['latitude', 'longitude']]

# Graphs
data = df[~df['price_display'].isna()]
mapbox = plot_map(data)
availability = plot_availability(df)
two_d = plot_review_price(df)
three_d = plot_3d_review_price(df)

# Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.Img(src="assets/logoaltotech-3-96x109.png"),
        html.H1("Hotel Dash"),
        html.P("Visualize hotel's business performance with "
               "data science and interactive data visualization platform"),
        html.Label("Price Range", className='dropdown-labels'),
        dcc.Dropdown(id='price-dropdown', className='dropdown', multi=False,
                     options=[
                         {'label': 'High', 'value': 300},
                         {'label': 'Low', 'value': 100}
                     ],
                     value=300),
        html.Label("Review Counts", className='dropdown-labels'),
        dcc.Dropdown(id='review-dropdown', className='dropdown', multi=False,
                     options=[
                         {'label': '10', 'value': 10},
                         {'label': '100', 'value': 100}
                     ],
                     value=10),
        html.Button(id='update-button', children="Apply Filter"),
        html.Div([
                html.Label("Clustering Algorithm", className='other-labels'),
                dcc.Dropdown(id='cluster-dropdown', className='dropdown',
                             options=[
                                 {'label': 'KMeans', 'value': 'KMeans'},
                                 {'label': 'DBSCAN', 'value': 'DBSCAN'}
                             ],
                             value='KMeans'),
                html.Label("Number of Clusters", className='other-labels'),
                dcc.Slider(id='n-slider', min=5, max=10, step=1, value=8),
                html.Label("Fill Missing Data with Regressor?", className='other-labels'),
                daq.BooleanSwitch(id='regression-toggle', className='toggle', on=False, color="#52BE80"),
                html.Button(id='update-cluster', children="Apply Clusters")
            ], id='config-box')
    ], id='left-container'),
    html.Div([
        html.Div([
            dcc.Graph(id='mapbox', figure=mapbox)
        ], id='top-half'),
        html.Div([
            dcc.Graph(id='two-plot', figure=two_d),
            dcc.Graph(id='three-plot', figure=three_d)
        ], id='bottom-half'),
    ], id='right-container')
], id='container')


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
