import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class SpotifyAPI:
    def __init__(self):
        # Get credentials from environment variables or use placeholders
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID', 'your_client_id_here')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', 'your_client_secret_here')

        # Initialize Spotify client
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            self.authenticated = True
        except:
            self.sp = None
            self.authenticated = False

    def search_song(self, song_name, artist=None):
        """Search for a song on Spotify"""
        if not self.authenticated:
            return None

        query = f"{song_name}"
        if artist:
            query += f" artist:{artist}"

        try:
            results = self.sp.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                return {
                    'spotify_id': track['id'],
                    'name': track['name'],
                    'artists': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify']
                }
        except Exception as e:
            print(f"Error searching song: {e}")

        return None

    def get_song_details(self, song_name, artist=None):
        """Get detailed song information including album art and preview"""
        return self.search_song(song_name, artist)

    def get_multiple_songs_details(self, songs_list):
        """Get details for multiple songs"""
        results = []
        for song in songs_list:
            if isinstance(song, dict):
                song_name = song.get('track_name', '')
                artist = song.get('artists', '')
            else:
                # Assume it's a string "song - artist"
                parts = song.split(' - ', 1)
                song_name = parts[0]
                artist = parts[1] if len(parts) > 1 else ''

            details = self.get_song_details(song_name, artist)
            if details:
                results.append({**song, **details} if isinstance(song, dict) else details)
            else:
                # If Spotify API fails, return basic info
                if isinstance(song, dict):
                    results.append(song)
                else:
                    results.append({
                        'name': song_name,
                        'artists': artist,
                        'album_image': None,
                        'preview_url': None,
                        'external_url': None
                    })

        return results

# Global Spotify API instance
spotify_api = SpotifyAPI()