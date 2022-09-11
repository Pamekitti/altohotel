import plotly.express as px
import plotly.figure_factory as ff

color = 'Aggrnyl'
mapbox_access_token = 'pk.eyJ1IjoicGFtZWtpdHRpIiwiYSI6ImNsN3J1M3Q3MTBpczUzb284YXh1ZmtqMzgifQ.CqCWrWGetLG4oR3T0rrZUw'
px.set_mapbox_access_token(mapbox_access_token)

# Plot Price Distribution
def plot_price_dis(df):
    group_labels = ['price_display', 'price_original']
    x1 = df['price_display'].dropna()
    x2 = df['price_original'].dropna()
    colors = ['#393E46', '#2BCDC1']
    fig = ff.create_distplot([x1,x2], group_labels, bin_size=.5, curve_type='normal', colors=colors)
    fig.update_layout(title_text='Price Distribution')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


# Price, Review Score, Review Count Scatter Plot
def plot_review_price(df, regressor=False):
    if regressor:
        X = "price_regressor"
    else:
        X = "price"
    fig = px.scatter(df, x=X, y="review_score", color="review_count",
                     hover_data=['review_count', 'name'], color_continuous_scale=color)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    return fig


# In 3D Plot
def plot_3d_review_price(df, regressor=False):
    if regressor:
        X = "price_regressor"
    else:
        X = "price"
    fig = px.scatter_3d(df, x=X, y="review_score", z="review_count", color="review_score",
                        color_continuous_scale=color, hover_data=['review_count', 'name'])
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    return fig


# Map Box Plot with color on review_count and size on price
def plot_map(df, regressor=False):
    if regressor:
        X = "price_regressor"
        data = df
    else:
        X = "price"
        data = df[~df['price'].isna()]
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color_continuous_scale=color,
                            color="review_count", size_max=10, zoom=10, size=X,
                            hover_data=['name', 'review_score'])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.update_layout(title_text='Map')
    return fig


# Plot Clustered data
def plot_cluster(df, algorithm_n):
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color_continuous_scale='jet',
                            color=algorithm_n, size_max=10, zoom=10,
                            hover_data=['name', 'review_score', 'review_count'])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.update_layout(title_text='Map')
    return fig


# Map Box Availability
def plot_availability(df):
    fig = px.scatter_mapbox(df.fillna(0), lat="latitude", lon="longitude",
                            color="availability", color_continuous_scale='RdYlBu', zoom=12)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


