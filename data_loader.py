#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

def load_data():
    data_by_genres = pd.read_csv('/Users/izzahalzahri/Desktop/data/data_by_genres.csv')
    data_by_artist = pd.read_csv('/Users/izzahalzahri/Desktop/data/data_by_artist.csv')
    data_by_year = pd.read_csv('/Users/izzahalzahri/Desktop/data/data_by_year.csv')
    data_w_genres = pd.read_csv('/Users/izzahalzahri/Desktop/data/data_w_genres.csv')
    data = pd.read_csv('/Users/izzahalzahri/Desktop/data/data.csv')

    return data_by_genres, data_by_artist, data_by_year, data_w_genres, data

def preprocess_data(data, data_w_genres):
    # Basic preprocessing
    data = data.dropna()
    data.drop_duplicates(inplace=True)
    data['year'] = pd.DatetimeIndex(data['release_date']).year
    
    # One-hot encode genres in the data_w_genres dataset
    data_w_genres_encoded = pd.get_dummies(data_w_genres, columns=['genres'])
    
    # Assigning random user IDs for testing purposes
    num_users = 10  # Example number of users
    user_ids = np.random.choice(range(1, num_users + 1), len(data))
    data['user_id'] = user_ids

    return data, data_w_genres_encoded
