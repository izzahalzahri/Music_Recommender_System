#!/usr/bin/env python
# coding: utf-8

# In[2]:


def recommend_based_on_popularity(data, n_recommendations=5):
    # Recommend the most popular songs
    popular_data = data.sort_values(by='popularity', ascending=False)
    return popular_data.head(n_recommendations)


