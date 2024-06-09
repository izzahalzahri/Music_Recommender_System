from content_based_recommender import recommend_songs_by_keyword
from collaborative_filtering import collaborative_filtering_recommendations

def hybrid_recommendations(data, user_id, keyword, n_recommendations=5):
    content_recommendations = recommend_songs_by_keyword(data, keyword, n_recommendations)
    collaborative_recommendations = collaborative_filtering_recommendations(data, user_id, n_recommendations)
    
    combined_recommendations = pd.concat([content_recommendations, collaborative_recommendations]).drop_duplicates()
    
    return combined_recommendations.head(n_recommendations)
