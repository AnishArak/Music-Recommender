# AI-Based Personalized Music Recommendation System

A modern, responsive web application that recommends similar songs using Machine Learning and Spotify API integration. Built with Flask, Python, and featuring a beautiful glassmorphism UI.

## 🎵 Features

- **Smart Recommendations**: Content-based filtering using cosine similarity on audio features
- **Mood-Based Discovery**: Explore music by mood (Happy, Sad, Chill, Workout, Romantic)
- **Spotify Integration**: Real-time album art, previews, and direct Spotify links
- **Search Suggestions**: Autocomplete song search functionality
- **Responsive Design**: Modern glassmorphism UI that works on all devices
- **Educational Content**: Detailed explanations of ML algorithms and recommendation systems

## 🚀 Tech Stack

### Backend
- **Python Flask** - Web framework
- **Pandas & NumPy** - Data processing
- **Scikit-learn** - Machine learning algorithms
- **Spotipy** - Spotify Web API integration

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with glassmorphism
- **JavaScript** - Interactive functionality

### Machine Learning
- **Content-Based Filtering** - Song similarity based on audio features
- **Cosine Similarity** - Distance metric for recommendations
- **Feature Scaling** - Normalized audio feature vectors

## 📊 Dataset

Uses the Spotify Tracks Dataset containing:
- 114,000+ songs
- Audio features: danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo
- Metadata: artist, album, popularity, genre

## 🏗️ Project Structure

```
music-recommender/
│
├── app.py                          # Flask application
├── recommendation.py               # ML recommendation engine
├── spotify_api.py                  # Spotify API integration
├── requirements.txt                # Python dependencies
├── dataset/
│   └── spotify_songs.csv          # Song dataset
├── templates/
│   ├── index.html                 # Home page
│   ├── about.html                 # About page
│   └── contact.html               # Contact page
├── static/
│   ├── css/
│   │   └── style.css              # Stylesheets
│   ├── js/
│   │   └── script.js              # JavaScript
│   └── images/                    # Static images
└── README.md                      # Documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Spotify Developer Account (for API access)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd music-recommender
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your Client ID and Client Secret
4. Set environment variables:
```bash
export SPOTIFY_CLIENT_ID='your_client_id'
export SPOTIFY_CLIENT_SECRET='your_client_secret'
```
Or create a `.env` file in the project root.

### 5. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🎯 Usage

### Song Recommendations
1. Enter a song name in the search bar
2. Get 5 similar song recommendations based on audio features
3. Click preview to listen or open in Spotify

### Mood-Based Recommendations
1. Click on mood buttons (Happy, Sad, Chill, Workout, Romantic)
2. Get curated song recommendations for that mood

### Search Suggestions
- Start typing a song name for autocomplete suggestions
- Click on suggestions to select

## 🧠 Machine Learning Details

### Content-Based Filtering
- Analyzes song audio features to find similarities
- No user history required - works with single song input
- Scales well with large datasets

### Audio Features Used
- **Danceability**: How suitable for dancing
- **Energy**: Intensity and activity level
- **Key**: Musical key of the track
- **Loudness**: Overall loudness in decibels
- **Mode**: Major/minor modality
- **Speechiness**: Presence of spoken words
- **Acousticness**: Acoustic vs electronic
- **Instrumentalness**: Vocal content presence
- **Liveness**: Live performance likelihood
- **Valence**: Musical positiveness
- **Tempo**: Estimated tempo in BPM

### Cosine Similarity
- Measures angle between song feature vectors
- Values range from -1 to 1 (1 = identical)
- Higher similarity = better recommendations

## 🎨 UI Features

- **Glassmorphism Design**: Modern frosted glass effects
- **Dark Theme**: Easy on the eyes
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Smooth Animations**: CSS transitions and transforms
- **Interactive Elements**: Hover effects and loading states

## 📱 API Endpoints

### GET `/api/search_suggestions`
Returns autocomplete suggestions for song search.

**Parameters:**
- `q`: Search query

### POST `/api/recommend`
Returns song recommendations based on input song.

**Body:**
```json
{
  "song_name": "Song Name"
}
```

### POST `/api/recommend_mood`
Returns mood-based song recommendations.

**Body:**
```json
{
  "mood": "happy"
}
```

### GET `/api/song_details`
Returns detailed song information from Spotify.

**Parameters:**
- `song`: Song name
- `artist`: Artist name (optional)

## 🚀 Deployment

### Local Deployment
```bash
python app.py
```

### Production Deployment
Consider using:
- **Gunicorn** for WSGI server
- **Nginx** as reverse proxy
- **Docker** for containerization
- **Heroku/AWS/GCP** for cloud hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Spotify for providing the Web API
- Kaggle for the Spotify Tracks Dataset
- Font Awesome for icons
- Google Fonts for typography

## 📞 Contact

For questions or feedback:
- Email: contact@aimusicrecommender.com
- GitHub Issues: Create an issue in this repository

---

**Built with ❤️ for Advanced Machine Learning coursework**