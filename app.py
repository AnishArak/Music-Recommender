from flask import Flask, render_template, request, jsonify
from recommendation import recommender
from spotify_api import spotify_api
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint for song recommendations"""
    try:
        data = request.get_json()
        song_name = data.get('song_name', '').strip()

        if not song_name:
            return jsonify({'error': 'Please provide a song name'}), 400

        # Get recommendations from ML model
        result = recommender.recommend(song_name)

        if 'error' in result:
            return jsonify(result), 404

        # Enhance with Spotify data
        enhanced_recommendations = spotify_api.get_multiple_songs_details(result['recommendations'])

        return jsonify({
            'query_song': result['query_song'],
            'recommendations': enhanced_recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend_mood', methods=['POST'])
def recommend_mood():
    """API endpoint for mood-based recommendations"""
    try:
        data = request.get_json()
        mood = data.get('mood', '').strip()

        if not mood:
            return jsonify({'error': 'Please provide a mood'}), 400

        # Get mood-based recommendations
        result = recommender.recommend_by_mood(mood)

        if 'error' in result:
            return jsonify(result), 404

        # Enhance with Spotify data
        enhanced_recommendations = spotify_api.get_multiple_songs_details(result['recommendations'])

        return jsonify({
            'mood': result['mood'],
            'recommendations': enhanced_recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search_suggestions', methods=['GET'])
def search_suggestions():
    """API endpoint for search suggestions"""
    try:
        query = request.args.get('q', '').strip()
        suggestions = recommender.get_search_suggestions(query)
        return jsonify({'suggestions': suggestions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/song_details', methods=['GET'])
def song_details():
    """API endpoint to get song details from Spotify"""
    try:
        song_name = request.args.get('song', '').strip()
        artist = request.args.get('artist', '').strip()

        if not song_name:
            return jsonify({'error': 'Please provide a song name'}), 400

        details = spotify_api.get_song_details(song_name, artist)
        if details:
            return jsonify(details)
        else:
            return jsonify({'error': 'Song not found on Spotify'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)