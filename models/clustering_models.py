from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import numpy as np


class Clusterer:
    def __init__(self, algorithm, min_cluster, max_cluster):
        self.algorithm = algorithm  # KMeans, DBSCAN, AgglomerativeClustering
        self.min_cluster = min_cluster
        self.max_cluster = max_cluster
        self.model_list = []
        self.metric = []
        self.inertia = []
        self.x = None

    def train(self, x):
        self.x = x
        metric = []  # metrics: silhouette score
        inertia = []  # find elbow with SSE plot
        model_list = []
        print('#'*25)
        print(f'Clustering with {self.algorithm}...')
        for cluster in range(self.min_cluster, self.max_cluster+1):
            if self.algorithm == 'KMeans':
                model = KMeans(n_clusters=cluster)
            if self.algorithm == 'AgglomerativeClustering':
                model = AgglomerativeClustering(n_clusters=cluster, linkage='complete')
            if self.algorithm == 'SpectralClustering':
                model = SpectralClustering(n_clusters=cluster)
            cluster_labels = model.fit_predict(x)
            silhouette_avg = silhouette_score(x, cluster_labels)
            metric.append(silhouette_avg)
            if self.algorithm == 'KMeans':
                inertia.append(model.inertia_)
                print(f'[{cluster} cluster]     train-silhouette:{round(silhouette_avg, 4)}      train-inertia:{round(model.inertia_, 4)}')
            else:
                print(f'[{cluster} cluster]     train-silhouette:{round(silhouette_avg, 4)}')
            model_list.append(model)

        self.model_list = model_list
        self.metric = metric
        self.inertia = inertia

    def silhouette_plot(self):
        plt.figure(figsize=(17, 6))
        sns.set_style("darkgrid")
        plt.title(f'Silhouette score for different number of clusters', fontsize=14, fontweight="bold")
        plt.xlabel('Clusters')
        plt.ylabel('Silhouette')
        plt.plot((range(self.min_cluster, self.max_cluster + 1)), self.metric, marker='o')
        plt.show()

    def sse_plot(self):
        plt.figure(figsize=(17, 6))
        sns.set_style("darkgrid")
        plt.title('Distortion values for different number of clusters for Kmeans', fontsize=14, fontweight="bold")
        plt.xlabel('Clusters')
        plt.ylabel('SSE')
        plt.plot((range(self.min_cluster, self.max_cluster + 1)), self.inertia, marker='o')
        plt.show()

    def plot_full_results(self):
        n_rows = self.max_cluster - self.min_cluster + 1
        fig, axs = plt.subplots(n_rows, 2)
        fig.set_size_inches(18, 4*n_rows)
        for i, n_clusters in enumerate(range(self.min_cluster, self.max_cluster + 1)):
            model = self.model_list[i]
            axs[i,0].set_xlim([-0.1, 1])
            axs[i,0].set_ylim([0, len(self.x) + (n_clusters + 1) * 10])
            cluster_labels = model.fit_predict(self.x)
            silhouette_avg = silhouette_score(self.x, cluster_labels)
            sample_silhouette_values = silhouette_samples(self.x, cluster_labels)

            y_lower = 10
            for j in range(n_clusters):
                ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == j]
                ith_cluster_silhouette_values.sort()
                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.nipy_spectral(float(j) / n_clusters)
                axs[i,0].fill_betweenx(
                    np.arange(y_lower, y_upper),
                    0,
                    ith_cluster_silhouette_values,
                    facecolor=color,
                    edgecolor=color,
                    alpha=0.7,
                )
                axs[i,0].text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
                y_lower = y_upper + 10

            axs[i,0].set_ylabel(f"{n_clusters} Clusters")
            axs[i,0].axvline(x=silhouette_avg, color="red", linestyle="--")

            axs[i,0].set_yticks([])
            axs[i,0].set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
            colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
            axs[i,1].scatter(
                self.x.iloc[:, 0], self.x.iloc[:, 1], marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
            )
        plt.show()

