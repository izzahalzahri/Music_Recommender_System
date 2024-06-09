import pandas as pd
import numpy as np
from spotify_integration import search_tracks

def recommend_with_diversity(data, keyword, n_recommendations=20):
    # Search tracks on Spotify
    spotify_recommendations = search_tracks(keyword, n_recommendations=n_recommendations)

    # Content-based recommendations from the dataset
    content_recommendations = data[data['name'].str.contains(keyword, case=False, na=False)]
    
    # Calculate the number of recommendations to take from each set
    n_content_recommendations = min(n_recommendations // 2, len(content_recommendations))
    n_diverse_recommendations = min(n_recommendations - n_content_recommendations, len(content_recommendations))
    
    # Ensure diversity by including a mix of popular and less popular songs
    top_content_recommendations = content_recommendations.sort_values(by='popularity', ascending=False).head(n_content_recommendations)
    diverse_recommendations = content_recommendations.sample(n=n_diverse_recommendations)
    
    # Combine the dataset recommendations
    dataset_recommendations = pd.concat([top_content_recommendations, diverse_recommendations]).drop_duplicates().head(n_recommendations)
    
    # Combine with Spotify recommendations
    final_recommendations = pd.concat([spotify_recommendations, dataset_recommendations]).drop_duplicates().head(n_recommendations)
    
    return final_recommendations
