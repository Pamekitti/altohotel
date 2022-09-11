from preprocessing.graphs import *
import pandas as pd
import dash
from dash import dcc, html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER

df = pd.read_csv('csv_files/clustered_hotel_regressor_filled.csv')
print(f'Date contains {df.shape[0]} rows of hotels in Bangkok')

# Graphs
mapbox = plot_map(df)
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
        html.Label("Price Range (USD)", className='dropdown-labels'),
        dcc.RangeSlider(0, 1000, id='price-range', value=[0, 1000],
                        tooltip={"placement": "bottom", "always_visible": True}),
        html.Label("Rating Range", className='dropdown-labels'),
        dcc.RangeSlider(0, 5, id='review-range', value=[0, 5],
                        tooltip={"placement": "bottom", "always_visible": True}),
        html.Button(id='update-button', children="Apply Filter"),
        html.Div([
                html.Label("Clustering Algorithm", className='other-labels'),
                dcc.Dropdown(id='cluster-dropdown', className='dropdown',
                             options=[
                                 {'label': 'None', 'value': 'none'},
                                 {'label': 'KMeans', 'value': 'kmeans'},
                                 {'label': 'Agglomerative Clustering', 'value': 'agglomerative'},
                                 {'label': 'Spectral Clustering', 'value': 'spectral'},
                                 {'label': 'DBSCAN', 'value': 'DBSCAN'}
                             ],
                             value='none'),
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


@app.callback(
    [Output(component_id='mapbox',
            component_property='figure'),
     Output(component_id='two-plot',
            component_property='figure'),
     Output(component_id='three-plot',
            component_property='figure')],
    [State(component_id='price-range',
           component_property='value'),
     State(component_id='review-range',
           component_property='value'),
     Input(component_id='update-button',
           component_property='n_clicks'),
     State(component_id='cluster-dropdown',
           component_property='value'),
     State(component_id='n-slider',
           component_property='value'),
     Input(component_id='update-cluster',
           component_property='n_clicks'),
     Input(component_id='regression-toggle',
           component_property='on')
     ]
)
def update_output(price_range, review_range, filter_clicks, cluster_algorithm, cluster_n, cluster_clicks, regressor_on):
    dff = df.copy()
    fig1 = mapbox
    fig2 = two_d
    fig3 = three_d
    if filter_clicks is not None:
        if filter_clicks > 0:
            dff = dff[dff['price'].between(price_range[0], price_range[1])]
            dff = dff[dff['review_score'].between(review_range[0], review_range[1])]
            fig1 = plot_map(dff)
            fig2 = plot_review_price(dff)
            fig3 = plot_3d_review_price(dff)
    if (cluster_clicks is not None) and (cluster_algorithm != 'none'):
        if cluster_clicks > 0:
            if regressor_on:
                fig2 = plot_review_price(dff, regressor=True)
                fig3 = plot_3d_review_price(dff, regressor=True)
            fig1 = plot_cluster(dff, f'{cluster_algorithm}_{cluster_n}')

    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
