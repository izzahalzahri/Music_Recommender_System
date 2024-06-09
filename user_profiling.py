#!/usr/bin/env python
# coding: utf-8

# In[2]:


from sklearn.cluster import KMeans
import pandas as pd

def extract_user_features(data):
    # Extract relevant features for clustering users
    features = data[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
    return features

def cluster_users(data, n_clusters=5):
    # Cluster users based on their music preferences using K-means
    features = extract_user_features(data)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(features)
    return data, kmeans


