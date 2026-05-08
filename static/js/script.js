// DOM Elements
const songSearch = document.getElementById('songSearch');
const searchBtn = document.getElementById('searchBtn');
const suggestions = document.getElementById('suggestions');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const loading = document.getElementById('loading');
const moodButtons = document.querySelectorAll('.mood-btn');

// Search functionality
let searchTimeout;
let currentAudio = null;

songSearch.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    const query = this.value.trim();

    if (query.length < 2) {
        suggestions.style.display = 'none';
        suggestions.innerHTML = '';
        return;
    }

    searchTimeout = setTimeout(() => {
        fetchSuggestions(query);
    }, 300);
});

songSearch.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

searchBtn.addEventListener('click', performSearch);

// Mood buttons
moodButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        const mood = this.getAttribute('data-mood');
        recommendByMood(mood);
    });
});

// Functions
async function fetchSuggestions(query) {
    try {
        const response = await fetch(`/api/search_suggestions?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.suggestions && data.suggestions.length > 0) {
            displaySuggestions(data.suggestions);
        } else {
            suggestions.style.display = 'none';
        }
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        suggestions.style.display = 'none';
    }
}

function displaySuggestions(suggestionsList) {
    suggestions.innerHTML = '';
    suggestionsList.forEach(item => {
        const div = document.createElement('div');
        div.className = 'suggestion-item';
        div.textContent = item.search_text;
        div.addEventListener('click', () => {
            songSearch.value = item.search_text;
            suggestions.style.display = 'none';
            performSearch();
        });
        suggestions.appendChild(div);
    });
    suggestions.style.display = 'block';
}

async function performSearch() {
    const songName = songSearch.value.trim();
    if (!songName) {
        alert('Please enter a song name');
        return;
    }

    showLoading();
    suggestions.style.display = 'none';
    suggestions.innerHTML = '';

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ song_name: songName })
        });

        const data = await response.json();
        hideLoading();

        if (response.ok) {
            displayRecommendations(data);
        } else {
            displayError(data.error);
        }
    } catch (error) {
        hideLoading();
        displayError('An error occurred while fetching recommendations');
        console.error('Error:', error);
    }
}

async function recommendByMood(mood) {
    showLoading();
    suggestions.style.display = 'none';
    suggestions.innerHTML = '';

    try {
        const response = await fetch('/api/recommend_mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mood: mood })
        });

        const data = await response.json();
        hideLoading();

        if (response.ok) {
            displayMoodRecommendations(data);
        } else {
            displayError(data.error);
        }
    } catch (error) {
        hideLoading();
        displayError('An error occurred while fetching recommendations');
        console.error('Error:', error);
    }
}

function displayRecommendations(data) {
    let html = `
        <div class="query-song">
            <h2>Recommendations for "${data.query_song.track_name}" by ${data.query_song.artists}</h2>
        </div>
        <div class="results-grid">
    `;

    data.recommendations.forEach(song => {
        const imageUrl = song.album_image || 'https://via.placeholder.com/300x300/667eea/ffffff?text=No+Image';
        const previewUrl = song.preview_url;
        const spotifyUrl = song.external_url || '#';

        html += `
            <div class="song-card">
                <img src="${imageUrl}" alt="${song.track_name}" class="song-image" onerror="this.src='https://via.placeholder.com/300x300/667eea/ffffff?text=No+Image'">
                <div class="song-info">
                    <h3>${song.track_name}</h3>
                    <p>${song.artists}</p>
                    <div class="song-meta">
                        <span>Popularity: ${song.popularity || 'N/A'}</span>
                        <span>Genre: ${song.track_genre || 'N/A'}</span>
                    </div>
                    <div class="song-actions">
                        ${previewUrl ? `<button class="btn btn-primary" onclick="playPreview('${previewUrl}')"><i class="fas fa-play"></i> Preview</button>` : ''}
                        <a href="${spotifyUrl}" target="_blank" class="btn btn-secondary"><i class="fab fa-spotify"></i> Open in Spotify</a>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayMoodRecommendations(data) {
    let html = `
        <div class="query-song">
            <h2>${data.mood.charAt(0).toUpperCase() + data.mood.slice(1)} Mood Recommendations</h2>
        </div>
        <div class="results-grid">
    `;

    data.recommendations.forEach(song => {
        const imageUrl = song.album_image || 'https://via.placeholder.com/300x300/667eea/ffffff?text=No+Image';
        const previewUrl = song.preview_url;
        const spotifyUrl = song.external_url || '#';

        html += `
            <div class="song-card">
                <img src="${imageUrl}" alt="${song.track_name}" class="song-image" onerror="this.src='https://via.placeholder.com/300x300/667eea/ffffff?text=No+Image'">
                <div class="song-info">
                    <h3>${song.track_name}</h3>
                    <p>${song.artists}</p>
                    <div class="song-meta">
                        <span>Popularity: ${song.popularity || 'N/A'}</span>
                        <span>Genre: ${song.track_genre || 'N/A'}</span>
                    </div>
                    <div class="song-actions">
                        ${previewUrl ? `<button class="btn btn-primary" onclick="playPreview('${previewUrl}')"><i class="fas fa-play"></i> Preview</button>` : ''}
                        <a href="${spotifyUrl}" target="_blank" class="btn btn-secondary"><i class="fab fa-spotify"></i> Open in Spotify</a>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayError(message) {
    resultsContent.innerHTML = `
        <div class="error-message" style="text-align: center; padding: 40px;">
            <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #ff6b6b; margin-bottom: 20px;"></i>
            <h3 style="color: #ff6b6b; margin-bottom: 10px;">Oops!</h3>
            <p style="color: rgba(255, 255, 255, 0.8);">${message}</p>
        </div>
    `;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function showLoading() {
    loading.style.display = 'flex';
}

function hideLoading() {
    loading.style.display = 'none';
}

function playPreview(url) {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    currentAudio = new Audio(url);
    currentAudio.play().catch(e => {
        alert('Unable to play preview. Please open in Spotify.');
    });
}

// Hide suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!songSearch.contains(e.target) && !suggestions.contains(e.target)) {
        suggestions.style.display = 'none';
        suggestions.innerHTML = '';
    }
});

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});