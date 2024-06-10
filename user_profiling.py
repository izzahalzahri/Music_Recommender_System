#!/usr/bin/env python
# coding: utf-8

# In[2]:

from sklearn.cluster import KMeans
import pandas as pd

# Sample dataset with track features
data = pd.DataFrame({
    'danceability': [0.5, 0.6, 0.7, 0.8, 0.9],
    'energy': [0.8, 0.7, 0.6, 0.5, 0.4],
    'loudness': [-5, -6, -7, -8, -9],
    'speechiness': [0.05, 0.04, 0.06, 0.07, 0.08],
    'acousticness': [0.1, 0.2, 0.3, 0.4, 0.5],
    'instrumentalness': [0.0, 0.1, 0.0, 0.0, 0.0],
    'liveness': [0.15, 0.16, 0.17, 0.18, 0.19],
    'valence': [0.6, 0.5, 0.4, 0.3, 0.2],
    'tempo': [120, 130, 140, 150, 160]
})

def extract_track_features(data):
    # Extract relevant features for clustering tracks
    features = data[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
    return features

def cluster_tracks(data, n_clusters=5):
    # Cluster tracks based on their features using K-means
    features = extract_track_features(data)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(features)
    return data, kmeans

# Cluster tracks
clustered_data, kmeans_model = cluster_tracks(data, n_clusters=3)
print(clustered_data)

# Example function to recommend tracks from a specific cluster
def recommend_tracks(clustered_data, target_cluster, n_recommendations=5):
    recommendations = clustered_data[clustered_data['cluster'] == target_cluster]
    return recommendations.head(n_recommendations)

# Recommend tracks from cluster 0
print(recommend_tracks(clustered_data, target_cluster=0))

#from sklearn.cluster import KMeans
#import pandas as pd

#def extract_user_features(data):
    # Extract relevant features for clustering users
  #  features = data[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
 #   return features

#def cluster_users(data, n_clusters=5):
    # Cluster users based on their music preferences using K-means
 #   features = extract_user_features(data)
  #  kmeans = KMeans(n_clusters=n_clusters, random_state=42)
   # data['cluster'] = kmeans.fit_predict(features)
    #return data, kmeans


