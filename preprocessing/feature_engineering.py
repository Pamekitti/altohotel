import pandas as pd
import numpy as np


def feature_engineer(df):
    # Amenities Hot Encoder
    amenities_list = list(set(df['amenities_0'].unique()) | set(df['amenities_1'].unique()) | set(df['amenities_2'].unique()))
    amenities_list.remove(np.nan)
    for amenity in amenities_list:
        have_list = []
        for i in range(df.shape[0]):
            l = list(df.loc[i, ['amenities_0', 'amenities_1', 'amenities_2']])
            if amenity in l:
                have_list.append(1)
            else:
                have_list.append(0)
        df[f'have_{amenity}'] = have_list
    df = df.drop(['amenities_0', 'amenities_1', 'amenities_2'], axis=1)

    # Cat Coder
    def cat_code(df: pd.DataFrame, col: str) -> pd.DataFrame:
        df[col] = df[col].fillna(0)
        df[col] = df[col].astype('category')
        df[col] = df[col].cat.codes
        df[col].value_counts()
        return df
    cat_cols = ['availability', 'free_cancel', 'pay_later', 'vip']
    for col in cat_cols:
        df = cat_code(df, col)

    # Room Left
    # mean_roomleft = round(df[(df['availability'] is True) & (df['roomleft'] > 0)]['roomleft'].mean())
    df['roomleft'] = df['roomleft'].fillna(4)
    df['roomleft'] = df['roomleft'] * df['availability']

    # Discount Price
    df['discount_percent'] = df['discount_percent'].fillna(0)
    df['price_original'] = df['price_original'].fillna(df['price_display'])
    df = df.drop(df[df['price_original'] >= 1000].index)

    # Reviews
    df = df.drop('review_superlative', axis=1)
    num = df[df['review_score'] == 0].shape[0]
    print(f'Dropping {num} rows with 0 review scores')
    df = df[df['review_score'] != 0]

    return df
