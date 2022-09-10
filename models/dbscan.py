from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class DBSCAN:
    def __init__(self, algorithm, epsilons):
        self.algorithm = algorithm  # KMeans, DBSCAN, AgglomerativeClustering
        self.epsilon = epsilons
        self.model_list = []
        self.metric = []
        self.outliers = []
        self.x = None

    def train(self, x):
        self.x = x
        metric = []  # metrics: silhouette score
        model_list = []
        number_of_outliers = []
        outlier_percent = []
        print('#'*25)
        print(f'Clustering with {self.algorithm}...')
        for epsilon in self.epsilon:
            model = DBSCAN(epsilons=epsilon, algorithm='auto')
            cluster_labels = model.fit(x)
            silhouette_avg = silhouette_score(x, cluster_labels)
            metric.append(silhouette_avg)
            number_of_outliers.append(np.sum(model.labels_ == -1))
            perc_outliers = 100 * np.sum(model.labels_ == -1) / len(model.labels_)
            outlier_percent.append(perc_outliers)
            print(f'[{epsilon} epsilon]     train-silhouette:{round(silhouette_avg, 4)}')
            model_list.append(model)

        self.model_list = model_list
        self.outliers = number_of_outliers
        self.metric = metric

    def plot_eps(self):
        plt.figure(figsize=(12, 6), dpi=100)
        sns.lineplot(x=self.epsilon, y=self.number_of_outliers)
        plt.ylabel("Percentage of Points Classified as Outliers")
        plt.xlabel("Epsilon Value")
        plt.title('Percentage of Points Classified as Outliers for Different Epsilon Values', fontsize='14',
                  fontweight='bold')

