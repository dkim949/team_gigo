import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pickle


def perform_kmeans(X, n_components=15, n_clusters=4):
    """
    Perform k-means clustering on the given dataset.

    Parameters
    ----------
    X : ndarray
        The input dataset.

    Returns
    -------
    model : KMeans
    clusters : ndarray
        The cluster assignments for each data point.
    """
    # Standardize the dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform PCA for dimensionality reduction
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    # Perform K-means clustering
    model = KMeans(n_clusters=n_clusters, init="k-means++")
    clusters = model.fit_predict(X_pca)

    return model, clusters
