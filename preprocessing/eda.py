import plotly.express as px
import plotly.figure_factory as ff


# Plot Price Distribution
def plot_price_dis(df):
    group_labels = ['price_display', 'price_original']
    x1 = df['price_display'].dropna()
    x2 = df['price_original'].dropna()
    colors = ['#393E46', '#2BCDC1']
    fig = ff.create_distplot([x1,x2], group_labels, bin_size=.5, curve_type='normal', colors=colors)
    fig.update_layout(title_text='Price Distribution')
    fig.show()


# Price, Review Score, Review Count Scatter Plot
def plot_review_price(df):
    fig = px.scatter(df, x="price_display", y="review_score", color="review_count", hover_data=['review_count'])
    fig.show()
    # In D Plot
    fig = px.scatter_3d(df, x="price_display", y="review_score", z="review_count", color="review_score", color_continuous_scale='matter', hover_data=['review_count'])
    fig.show()


# Map Box Plot with color on review_count and size on price
def plot_map(df):
    data = df[~df['price_display'].isna()]
    mapbox_access_token = 'pk.eyJ1IjoicGFtZWtpdHRpIiwiYSI6ImNsN3J1M3Q3MTBpczUzb284YXh1ZmtqMzgifQ.CqCWrWGetLG4oR3T0rrZUw'
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color_continuous_scale='matter',
                            color="review_count", size_max=15, zoom=10, size="price_display", hover_data=['name'])
    fig.show()


# Map Box Availability
def plot_availability(df):
    mapbox_access_token = 'pk.eyJ1IjoicGFtZWtpdHRpIiwiYSI6ImNsN3J1M3Q3MTBpczUzb284YXh1ZmtqMzgifQ.CqCWrWGetLG4oR3T0rrZUw'
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.scatter_mapbox(df.fillna(0), lat="latitude", lon="longitude",
                            color="availability", color_continuous_scale='RdYlBu', zoom=12)
    fig.show()


