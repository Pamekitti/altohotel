import pandas as pd


def get_hotel_data(src: str):
    df = pd.read_csv(src)
    # Drop first column
    df = df.drop(df.columns[0], axis=1)
    # Filter columns
    df = df[['hotel_name', 'hotel_latitude', 'hotel_longitude', 'highlight', 'award_year', 'area_name',
             'property_type', 'rating', 'count_reviwer', 'review_score', 'features', 'facilities']]
    # Rename some columns
    df = df.rename(columns={'hotel_name': 'name', 'hotel_latitude': 'lat', 'hotel_longitude': 'lon',
                            'property_type': 'type', 'area_name': 'area'})

    # Split string in hotel_name column
    df['name'] = df['name'].str.split("(").str[0]
    df['name'] = df['name'].str.split(" SHA").str[0]

    return df


def df_to_dd_options (df):
    dff = df[['name', 'lat', 'lon']]
    df_dict = dff.to_dict('records')
    dd_options = [dict(value=c["name"], label=c["name"]) for c in df_dict]
    dd_defaults = [o["value"] for o in dd_options]

    return df_dict, dd_options, dd_defaults


