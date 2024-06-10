import streamlit as st
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_integration import search_tracks, recommend_tracks_by_genre, recommend_playlists_by_track, get_all_genres


load_dotenv('spotify.env')

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))


import streamlit as st
from spotify_integration import search_tracks, recommend_tracks_by_genre, recommend_playlists_by_track, get_all_genres

# Set page configuration
st.set_page_config(page_title="Music Recommender", page_icon=":musical_note:", layout="wide")

# Load custom CSS
def load_css():
    st.markdown("""
        <style>
            body {
                background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
                font-family: 'Arial', sans-serif;
                color: #333;
            }
            .container {
                padding: 20px;
                background: #fff;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .search-bar {
                width: 100%;
                padding: 15px;
                border-radius: 25px;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .song-container, .playlist-container {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                padding: 10px;
                border-radius: 10px;
                background: #f9f9f9;
                transition: transform 0.3s ease;
            }
            .song-container:hover, .playlist-container:hover {
                transform: scale(1.02);
            }
            .song-image, .playlist-image {
                width: 50px;
                height: 50px;
                object-fit: cover;
                margin-right: 10px;
                border-radius: 5px;
            }
            .song-details, .playlist-details {
                flex-grow: 1;
            }
            .song-title, .playlist-title {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .song-artist, .playlist-description {
                font-size: 16px;
                color: #666;
                margin-bottom: 5px;
            }
            .song-popularity {
                font-size: 16px;
                color: #ff9900;
            }
        </style>
    """, unsafe_allow_html=True)

# Load custom CSS
load_css()

# Page title
st.title('🎧 Hybrid Music Recommender System with Diversity and Genre-Based Recommendations')

# Load genres from Spotify
genres = get_all_genres()

# User input for recommendations
st.header('🔍 Recommend Songs and Playlists')

input_type = st.radio('Select input type:', ('Genre', 'Song Title or Artist Name'))

if input_type == 'Genre':
    genre = st.selectbox('Select a genre', genres)
    if st.button('Recommend Songs and Playlists'):
        with st.spinner('Finding songs and playlists...'):
            # Recommend tracks by genre
            song_recommendations = recommend_tracks_by_genre(genre, n_recommendations=20)
            
        if not song_recommendations.empty:
            # Create two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### 🎵 Songs")
                for _, row in song_recommendations.iterrows():
                    st.markdown(f"""
                        <div class="song-container">
                            <img class="song-image" src="{row['album_cover']}" alt="{row['name']}">
                            <div class="song-details">
                                <div class="song-title"><a href="{row['url']}" target="_blank">{row['name']} by {row['artists']}</a></div>
                                <div class="song-artist">{row['artists']}</div>
                                <div class="song-popularity">Popularity: {'★' * (row['popularity'] // 20)}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.write("### 📜 Playlists")
                playlist_recommendations = []
                seen_playlists = set()  # To track and avoid duplicates
                for _, row in song_recommendations.iterrows():
                    playlists = recommend_playlists_by_track(row['name'], n_recommendations=2)
                    for playlist in playlists:
                        if playlist['url'] not in seen_playlists:
                            seen_playlists.add(playlist['url'])
                            playlist_recommendations.append(playlist)

                if playlist_recommendations:
                    for playlist in playlist_recommendations:
                        st.markdown(f"""
                            <div class="playlist-container">
                                <img class="playlist-image" src="{playlist['image']}" alt="{playlist['name']}">
                                <div class="playlist-details">
                                    <div class="playlist-title"><a href="{playlist['url']}" target="_blank">{playlist['name']}</a></div>
                                    <div class="playlist-description">{playlist['description']}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write(f"No playlists found including the selected songs.")
        else:
            st.write(f"No songs found for the genre '{genre}'.")

else:
    keyword = st.text_input('Enter a Song Title or Artist Name (e.g., "love" or "Adele")')

    if st.button('Recommend Songs and Playlists'):
        if keyword:
            with st.spinner('Finding songs and playlists...'):
                # Search for tracks on Spotify
                song_recommendations = search_tracks(keyword, n_recommendations=20)
                song_recommendations.drop_duplicates(subset=['name', 'artists'], inplace=True)
        
            if not song_recommendations.empty:
                # Create two columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("### 🎵 Songs")
                    for _, row in song_recommendations.iterrows():
                        st.markdown(f"""
                            <div class="song-container">
                                <img class="song-image" src="{row['album_cover']}" alt="{row['name']}">
                                <div class="song-details">
                                    <div class="song-title"><a href="{row['url']}" target="_blank">{row['name']} by {row['artists']}</a></div>
                                    <div class="song-artist">{row['artists']}</div>
                                    <div class="song-popularity">Popularity: {'★' * (row['popularity'] // 20)}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.write("### 📜 Playlists")
                    playlist_recommendations = []
                    seen_playlists = set()  # To track and avoid duplicates
                    for _, row in song_recommendations.iterrows():
                        playlists = recommend_playlists_by_track(row['name'], n_recommendations=2)
                        for playlist in playlists:
                            if playlist['url'] not in seen_playlists:
                                seen_playlists.add(playlist['url'])
                                playlist_recommendations.append(playlist)

                    if playlist_recommendations:
                        for playlist in playlist_recommendations:
                            st.markdown(f"""
                                <div class="playlist-container">
                                    <img class="playlist-image" src="{playlist['image']}" alt="{playlist['name']}">
                                    <div class="playlist-details">
                                        <div class="playlist-title"><a href="{playlist['url']}" target="_blank">{playlist['name']}</a></div>
                                        <div class="playlist-description">{playlist['description']}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.write(f"No playlists found including the selected songs.")
            else:
                st.write(f"No songs found with '{keyword}' in the title or artist name.")
        else:
            st.write("Please enter a song title or artist name.")

# To run the app:
# streamlit run app.py
