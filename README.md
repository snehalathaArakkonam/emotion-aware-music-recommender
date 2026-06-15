# Emotion-Aware Music Recommender 🎵

A real-time system that detects your emotion via webcam and recommends Spotify tracks accordingly.

## Features
- Real-time face & emotion detection (DeepFace)
- Spotify recommendations based on mood
- Mood history tracking with SQLite
- Streamlit UI with live preview

## Setup
1. `pip install -r requirements.txt`
2. `pip install deepface[all]`
3. Set Spotify API credentials as env vars
4. `streamlit run app.py`

## Environment Variables
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`

Built with ❤️ using Python, OpenCV, DeepFace & Spotify API.