# 🎵 Emotion-Aware Music Recommender System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)
![Spotify](https://img.shields.io/badge/Spotify-API-1DB954?style=for-the-badge&logo=spotify)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)
![DeepFace](https://img.shields.io/badge/DeepFace-Emotion%20AI-orange?style=for-the-badge)

**A real-time facial emotion detection system that recommends Spotify songs based on your current mood.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Configuration](#-configuration) • [Usage](#-usage) • [Architecture](#-architecture) • [API Reference](#-api-reference)

</div>

---

## 📌 Overview

The **Emotion-Aware Music Recommender** captures your facial expressions in real-time using your webcam, classifies your emotion using **DeepFace / FER**, maps that emotion to Spotify audio feature parameters, and fetches personalized song recommendations — all in seconds.

> **Built for placement portfolio demonstration** — showcasing full-stack integration of Computer Vision, ML, REST APIs, and Database Management.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 **Real-time Webcam Feed** | Live face capture using OpenCV |
| 🧠 **Emotion Detection** | DeepFace / FER classifies 7 emotions with confidence scoring |
| 🎯 **Confidence Threshold** | Only triggers recommendations when emotion confidence > 60% |
| 🎵 **Spotify Integration** | Maps emotions to audio features and fetches top 5 recommendations |
| 🖼️ **Album Art Display** | Shows song cards with album art and Spotify preview URLs |
| 📊 **Mood History** | SQLite tracks your mood over the last 7 days |
| 📝 **Lyrics Sentiment** | Optional Genius API integration for lyrics analysis |
| 🔁 **Fallback Handling** | Graceful handling when no face is detected |

---

## 🎭 Emotion → Music Mapping

| Emotion | Valence | Energy | Tempo | Danceability |
|---------|---------|--------|-------|--------------|
| 😄 **Happy** | 0.7 – 1.0 | 0.7 – 1.0 | 120 – 180 | 0.7 – 1.0 |
| 😢 **Sad** | 0.0 – 0.3 | 0.1 – 0.4 | 60 – 90 | 0.2 – 0.5 |
| 😠 **Angry** | 0.1 – 0.4 | 0.8 – 1.0 | 150 – 200 | 0.5 – 0.8 |
| 😐 **Neutral** | 0.4 – 0.6 | 0.4 – 0.6 | 90 – 120 | 0.4 – 0.6 |
| 😲 **Surprised** | 0.6 – 0.9 | 0.6 – 0.9 | 120 – 160 | 0.6 – 0.9 |
| 😨 **Fear** | 0.1 – 0.3 | 0.6 – 0.9 | 130 – 180 | 0.3 – 0.6 |
| 🤢 **Disgust** | 0.0 – 0.2 | 0.4 – 0.7 | 80 – 120 | 0.2 – 0.5 |

---

## 🖥️ Demo

```
📷 Webcam captures face
        ↓
🧠 DeepFace detects: HAPPY (confidence: 87%)
        ↓
🎵 Spotify API query → valence: 0.8, energy: 0.9, tempo: 140
        ↓
🎶 Top 5 Songs Recommended:
   1. Blinding Lights – The Weeknd         ▶ Preview
   2. Levitating – Dua Lipa                ▶ Preview
   3. Happy – Pharrell Williams            ▶ Preview
   4. Can't Stop the Feeling – Justin T.   ▶ Preview
   5. Uptown Funk – Bruno Mars             ▶ Preview
```

---

## 🗂️ Project Structure

```
emotion-aware-music-recommender/
│
├── app.py                        # Main Flask application
├── streamlit_app.py              # Alternative Streamlit UI
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── emotion_detector.py       # OpenCV + DeepFace face/emotion detection
│   ├── spotify_client.py         # Spotify API integration
│   ├── mood_mapper.py            # Emotion → audio features mapping
│   └── genius_client.py          # Genius API for lyrics (optional)
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py             # SQLite CRUD operations
│   └── models.py                 # Data models / schema
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── placeholder.png
│
├── templates/
│   ├── index.html                # Main UI
│   ├── history.html              # Mood history dashboard
│   └── components/
│       └── song_card.html
│
└── tests/
    ├── test_emotion_detector.py
    ├── test_spotify_client.py
    └── test_db_manager.py
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- Webcam / Camera device
- Spotify Developer Account → [Create App](https://developer.spotify.com/dashboard)
- Genius API Account → [Create App](https://genius.com/api-clients) *(optional)*

### Step 1 — Clone the Repository

```bash
git clone https://github.com/snehalathaArakkonam/emotion-aware-music-recommender.git
cd emotion-aware-music-recommender
```

### Step 2 — Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** DeepFace will auto-download model weights (~500MB) on first run.

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback

# Genius API (Optional - for lyrics sentiment)
GENIUS_ACCESS_TOKEN=your_genius_access_token_here

# App Settings
EMOTION_CONFIDENCE_THRESHOLD=0.60
FLASK_SECRET_KEY=your_random_secret_key_here
FLASK_DEBUG=True
DATABASE_PATH=database/mood_history.db
```

### Step 5 — Initialize the Database

```bash
python -c "from database.db_manager import init_db; init_db()"
```

### Step 6 — Run the Application

**Flask (Web UI):**
```bash
python app.py
```
Open → [http://localhost:5000](http://localhost:5000)

**Streamlit (Alternative UI):**
```bash
streamlit run streamlit_app.py
```
Open → [http://localhost:8501](http://localhost:8501)

---

## 📦 Requirements

```txt
# requirements.txt

# Web Framework
flask==2.3.3
streamlit==1.28.0

# Computer Vision & Emotion Detection
opencv-python==4.8.1.78
deepface==0.0.79
fer==22.5.1
tensorflow==2.13.0

# Spotify Integration
spotipy==2.23.0

# Database
# sqlite3 is built-in to Python

# Environment & Utilities
python-dotenv==1.0.0
requests==2.31.0
Pillow==10.0.1
numpy==1.24.3

# Lyrics Sentiment (Optional)
lyricsgenius==3.0.1
textblob==0.17.1
nltk==3.8.1

# Testing
pytest==7.4.3
```

---

## 🔧 Configuration

### Spotify App Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **Create App**
3. Set Redirect URI to `http://localhost:5000/callback`
4. Copy **Client ID** and **Client Secret** to `.env`

### DeepFace Emotion Model

The system uses `DeepFace` with the following configuration:

```python
# Supported backends: opencv, ssd, dlib, mtcnn, retinaface
DETECTOR_BACKEND = "opencv"   # Fastest, works offline

# Supported emotion models: VGG-Face, Facenet, DeepFace, ArcFace
EMOTION_MODEL = "VGG-Face"
```

### Emotion Confidence Threshold

Only emotions detected with **> 60% confidence** trigger song recommendations. This prevents false positives from poor lighting or partial face detection.

```python
EMOTION_CONFIDENCE_THRESHOLD = 0.60  # Configurable in .env
```

---

## 🚀 Usage

### 1. Start Detection

- Open the app and click **"Start Camera"**
- Ensure your face is well-lit and centered in frame
- The system detects your emotion within 1–2 seconds

### 2. View Recommendations

- Top 5 songs are displayed with:
  - 🎵 Song title & artist name
  - 🖼️ Album artwork
  - ▶️ 30-second Spotify preview link
  - 🔗 Open in Spotify button

### 3. Mood History

- Navigate to `/history` (Flask) or the **History tab** (Streamlit)
- View your emotion logs from the **last 7 days**
- Charts show mood frequency distribution and trends over time

### 4. Lyrics Sentiment (Optional)

- When enabled, the app fetches lyrics from Genius API
- Performs sentiment analysis using TextBlob
- Displays sentiment polarity alongside each song recommendation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│              Flask Web App  /  Streamlit App                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────▼───────────────────┐
        │           Core Processing             │
        │                                       │
        │  ┌─────────────┐  ┌───────────────┐  │
        │  │   OpenCV    │  │   DeepFace /  │  │
        │  │  Webcam     │→ │   FER Model   │  │
        │  │  Capture    │  │  (Emotion AI) │  │
        │  └─────────────┘  └──────┬────────┘  │
        │                          │            │
        │                  ┌───────▼────────┐   │
        │                  │  Mood Mapper   │   │
        │                  │ Emotion→Audio  │   │
        │                  │   Features     │   │
        │                  └───────┬────────┘   │
        └──────────────────────────┼────────────┘
                                   │
        ┌──────────────────────────▼────────────────────────┐
        │                  External APIs                      │
        │                                                     │
        │  ┌──────────────┐         ┌──────────────────────┐ │
        │  │  Spotify API │         │  Genius API           │ │
        │  │ Recommendations│       │ (Lyrics - Optional)   │ │
        │  └──────┬───────┘         └──────────────────────┘ │
        └─────────┼──────────────────────────────────────────┘
                  │
        ┌─────────▼──────────────┐
        │      SQLite DB          │
        │  Mood History (7 days)  │
        └────────────────────────┘
```

---

## 📡 API Reference

### Flask Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main UI — live webcam + recommendations |
| `GET` | `/history` | Mood history dashboard (last 7 days) |
| `POST` | `/detect` | Accepts base64 frame, returns emotion + confidence |
| `POST` | `/recommend` | Accepts emotion, returns top 5 Spotify songs |
| `GET` | `/mood-stats` | Returns JSON mood frequency stats |
| `GET` | `/callback` | Spotify OAuth callback |
| `GET` | `/health` | Health check endpoint |

### Sample `/detect` Request

```json
POST /detect
Content-Type: application/json

{
  "frame": "<base64_encoded_image>"
}
```

### Sample `/detect` Response

```json
{
  "status": "success",
  "emotion": "happy",
  "confidence": 0.87,
  "all_emotions": {
    "happy": 0.87,
    "neutral": 0.08,
    "sad": 0.03,
    "angry": 0.02
  },
  "face_detected": true,
  "threshold_met": true
}
```

### Sample `/recommend` Response

```json
{
  "status": "success",
  "emotion": "happy",
  "songs": [
    {
      "title": "Blinding Lights",
      "artist": "The Weeknd",
      "album": "After Hours",
      "album_art": "https://i.scdn.co/image/...",
      "preview_url": "https://p.scdn.co/mp3-preview/...",
      "spotify_url": "https://open.spotify.com/track/...",
      "valence": 0.83,
      "energy": 0.80,
      "tempo": 171.0
    }
  ]
}
```

---

## 🗄️ Database Schema

```sql
-- Mood History Table
CREATE TABLE mood_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion     TEXT NOT NULL,
    confidence  REAL NOT NULL,
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
    songs_json  TEXT,           -- JSON array of recommended song IDs
    session_id  TEXT
);

-- Session Aggregates Table
CREATE TABLE mood_sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT UNIQUE,
    dominant_mood   TEXT,
    start_time      DATETIME,
    end_time        DATETIME,
    total_detections INTEGER
);
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_emotion_detector.py -v

# Run with coverage report
pytest tests/ --cov=core --cov-report=html
```

---

## 🐛 Troubleshooting

### Camera Not Detected
```python
# In emotion_detector.py, change camera index
cap = cv2.VideoCapture(0)   # Try 0, 1, or 2
```

### DeepFace Model Download Fails
```bash
# Pre-download models manually
python -c "from deepface import DeepFace; DeepFace.build_model('Emotion')"
```

### Spotify Token Expired
```bash
# Delete cached token and re-authenticate
rm .cache-*
python app.py   # Re-triggers OAuth flow
```

### No Face Detected Fallback
When no face is found in frame, the system:
1. Displays a "No face detected" overlay on the video feed
2. Shows previously recommended songs (last known emotion)
3. Logs a `None` entry in mood history
4. Retries detection every 500ms

### Low Confidence Detection
If emotion confidence is below the 60% threshold:
1. The UI shows "Detecting emotion..." spinner
2. The system averages the last 3 frames before triggering
3. Falls back to `neutral` emotion after 5 consecutive low-confidence frames

---

## 🔐 Security

- API keys are stored in `.env` file (never committed to Git)
- `.gitignore` includes `.env`, `*.cache`, and `__pycache__`
- Spotify OAuth uses PKCE flow for secure token exchange
- SQLite database is local-only

---

## 🛣️ Roadmap

- [x] Real-time emotion detection via webcam
- [x] Spotify recommendations with audio features
- [x] Mood history tracking (SQLite)
- [x] Album art and preview URL display
- [x] Emotion confidence threshold filtering
- [x] Genius API lyrics sentiment (optional)
- [ ] Multi-face detection support
- [ ] Playlist auto-creation on Spotify
- [ ] Emotion trend notifications
- [ ] Docker containerization
- [ ] Mobile PWA support

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch → `git checkout -b feature/your-feature`
3. Commit changes → `git commit -m 'Add: your feature description'`
4. Push to branch → `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Snehalatha Arakkonam**

[![GitHub](https://img.shields.io/badge/GitHub-snehalathaArakkonam-black?style=flat&logo=github)](https://github.com/snehalathaArakkonam/emotion-aware-music-recommender)

---

## 🙏 Acknowledgements

- [DeepFace](https://github.com/serengil/deepface) — Face analysis library
- [Spotipy](https://spotipy.readthedocs.io/) — Spotify Web API Python client
- [OpenCV](https://opencv.org/) — Computer vision framework
- [FER](https://github.com/justinshenk/fer) — Facial Expression Recognition
- [LyricsGenius](https://lyricsgenius.readthedocs.io/) — Genius API Python wrapper

---

<div align="center">
⭐ Star this repo if you found it helpful for your placements!
</div>
