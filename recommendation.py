import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import os

class MusicRecommender:
    def __init__(self, sample_size=5000):
        self.sample_size = sample_size
        self.df = None
        self.similarity_matrix = None
        self.scaler = StandardScaler()
        self.feature_cols = ['danceability', 'energy', 'key', 'loudness', 'mode',
                           'speechiness', 'acousticness', 'instrumentalness',
                           'liveness', 'valence', 'tempo']
        self.load_data()
        self.preprocess_data()
        self.compute_similarity()

    def load_data(self):
        """Load the Spotify songs dataset and sample for efficiency"""
        dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'spotify_songs.csv')
        full_df = pd.read_csv(dataset_path)
        # Clean data
        full_df.dropna(subset=['track_name', 'artists'], inplace=True)
        # Sample a subset for recommendations
        self.df = full_df.sample(n=self.sample_size, random_state=42).reset_index(drop=True)
        # Create a combined title for searching
        self.df['search_title'] = self.df['track_name'] + ' - ' + self.df['artists']

    def preprocess_data(self):
        """Preprocess the data for recommendation"""
        # Select numerical features for similarity
        X = self.df[self.feature_cols].values
        # Scale the features
        self.X_scaled = self.scaler.fit_transform(X)

    def compute_similarity(self):
        """Compute cosine similarity matrix"""
        self.similarity_matrix = cosine_similarity(self.X_scaled)

    def recommend(self, song_name, n_recommendations=5):
        """Recommend similar songs based on song name"""
        # Find the song index
        song_idx = self.find_song_index(song_name)
        if song_idx is None:
            return {"error": "Song not found. Please try a different song name."}

        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[song_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top recommendations (excluding the song itself)
        recommendations = []
        for i, score in sim_scores[1:n_recommendations+1]:
            song_data = self.df.iloc[i]
            recommendations.append({
                'track_name': song_data['track_name'],
                'artists': song_data['artists'],
                'album_name': song_data.get('album_name', 'Unknown'),
                'popularity': int(song_data.get('popularity', 0)),
                'track_genre': song_data.get('track_genre', 'Unknown'),
                'similarity_score': round(float(score), 3)
            })

        return {
            'query_song': {
                'track_name': self.df.iloc[song_idx]['track_name'],
                'artists': self.df.iloc[song_idx]['artists']
            },
            'recommendations': recommendations
        }

    def find_song_index(self, song_name):
        """Find the index of a song by name (case insensitive partial match)"""
        song_name_lower = song_name.lower().strip()
        # First try exact match
        exact_match = self.df[self.df['search_title'].str.lower() == song_name_lower]
        if not exact_match.empty:
            return exact_match.index[0]

        # Then try partial match in track name
        partial_match = self.df[self.df['track_name'].str.lower().str.contains(song_name_lower, na=False)]
        if not partial_match.empty:
            return partial_match.index[0]

        # Then try partial match in artists
        artist_match = self.df[self.df['artists'].str.lower().str.contains(song_name_lower, na=False)]
        if not artist_match.empty:
            return artist_match.index[0]

        return None

    def recommend_by_mood(self, mood, n_recommendations=5):
        """Recommend songs based on mood"""
        mood_filters = {
            'happy': lambda df: (df['valence'] > 0.6) & (df['energy'] > 0.6),
            'sad': lambda df: (df['valence'] < 0.4) & (df['energy'] < 0.4),
            'chill': lambda df: (df['energy'] < 0.5) & (df['acousticness'] > 0.5),
            'workout': lambda df: (df['energy'] > 0.7) & (df['tempo'] > 120),
            'romantic': lambda df: (df['valence'] > 0.5) & (df['acousticness'] > 0.4)
        }

        if mood not in mood_filters:
            return {"error": "Invalid mood. Choose from: happy, sad, chill, workout, romantic"}

        filtered_df = self.df[mood_filters[mood](self.df)]
        if filtered_df.empty:
            return {"error": f"No songs found for mood: {mood}"}

        # Sample random songs from the filtered dataset
        sampled_songs = filtered_df.sample(min(n_recommendations, len(filtered_df)))

        recommendations = []
        for _, song_data in sampled_songs.iterrows():
            recommendations.append({
                'track_name': song_data['track_name'],
                'artists': song_data['artists'],
                'album_name': song_data.get('album_name', 'Unknown'),
                'popularity': int(song_data.get('popularity', 0)),
                'track_genre': song_data.get('track_genre', 'Unknown'),
                'mood': mood
            })

        return {
            'mood': mood,
            'recommendations': recommendations
        }

    def get_search_suggestions(self, query, limit=10):
        """Get search suggestions for autocomplete"""
        if not query:
            return []

        query_lower = query.lower()
        # Find songs that match the query
        matches = self.df[
            self.df['track_name'].str.lower().str.contains(query_lower, na=False) |
            self.df['artists'].str.lower().str.contains(query_lower, na=False)
        ]

        suggestions = []
        for _, song in matches.head(limit).iterrows():
            suggestions.append({
                'track_name': song['track_name'],
                'artists': song['artists'],
                'search_text': f"{song['track_name']} - {song['artists']}"
            })

        return suggestions

# Global recommender instance
recommender = MusicRecommender()