from models.clustering_models import Clusterer
from preprocessing.clean_data import clean_hotel_data
from preprocessing.feature_engineering import feature_engineer
import pandas as pd

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
visualize_silhouette_results = True
for algorithm in ['KMeans', 'AgglomerativeClustering', 'SpectralClustering']:
    clusterer = Clusterer(algorithm=algorithm, min_cluster=5, max_cluster=10)
    clusterer.train(train)
    if visualize_silhouette_results:
        clusterer.silhouette_plot()




