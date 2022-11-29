import plotly.express as px
import plotly.graph_objects as go

color = 'Aggrnyl'
mapbox_token = 'pk.eyJ1IjoicGFtZWtpdHRpIiwiYSI6ImNsN3J1M3Q3MTBpczUzb284YXh1ZmtqMzgifQ.CqCWrWGetLG4oR3T0rrZUw'
px.set_mapbox_access_token(mapbox_token)


def build_map(df, filter=False, name=None):

    if filter:
        lat, lon = df[df['name'] == name][['lat', 'lon']].values[0]
        fig = px.scatter_mapbox(df, lat='lat', lon='lon', zoom=18,
                                text='name', labels={'name': 'Hotel Name',
                                                     'lat': 'Latitude',
                                                     'lon': 'Longitude'},
                                center=dict(lat=lat,
                                            lon=lon))
    else:
        fig = px.scatter_mapbox(df, lat="lat", lon="lon", zoom=11,
                                text='name', labels={'name': 'Hotel Name',
                                                     'lat': 'Latitude',
                                                     'lon': 'Longitude'},
                                center=dict(lat=df['lat'].mean(),
                                            lon=df['lon'].mean()))

    # fig.update_traces(cluster=dict(enabled=True))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      hoverlabel=dict(bgcolor='white', font_size=12),
                      width=1080, height=690)
    fig.update_traces(marker=dict(size=15, symbol='marker'),
                      textposition="bottom right", textfont_size=14,
                      )


    return fig







