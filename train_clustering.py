from models.clustering_models import Clusterer
from preprocessing.clean_data import clean_hotel_data
from preprocessing.feature_engineering import feature_engineer
import pandas as pd

'''
Generated labeled (Clustered) data for dashboard
'''
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

models = {'KMeans': 'kmeans',
          'AgglomerativeClustering': 'agglomerative',
          'SpectralClustering': 'spectral'}

# True will show model evaluate plots
visualize_silhouette_results = False

# Train/Predict cluster labels and append results to DataFrame
for algorithm in models:
    clusterer = Clusterer(algorithm=algorithm, min_cluster=5, max_cluster=10)
    clusterer.train(train)
    if visualize_silhouette_results:
        clusterer.silhouette_plot()
    for i in range(clusterer.max_cluster - clusterer.min_cluster + 1):
        df[f'{models[algorithm]}_{i + clusterer.min_cluster}'] = clusterer.prediction[i]

df.to_csv('csv_files/clustered_hotel.csv')





