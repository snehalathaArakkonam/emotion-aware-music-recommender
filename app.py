import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import datetime
import time
import os

# ====================== CONFIG ======================
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    st.error("❌ Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET as environment variables.")
    st.stop()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

EMOTION_MAPPING = {
    "happy": {"valence": (0.7, 1.0), "energy": (0.6, 1.0), "tempo": (100, 160)},
    "sad": {"valence": (0.0, 0.4), "energy": (0.0, 0.4), "tempo": (60, 110)},
    "angry": {"valence": (0.3, 0.7), "energy": (0.7, 1.0), "tempo": (120, 180)},
    "neutral": {"valence": (0.4, 0.7), "energy": (0.3, 0.7), "tempo": (80, 140)},
    "surprise": {"valence": (0.5, 0.9), "energy": (0.6, 1.0), "tempo": (110, 170)},
}

# ====================== DATABASE ======================
def init_db():
    conn = sqlite3.connect('mood_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS moods
                 (id INTEGER PRIMARY KEY, timestamp TEXT, emotion TEXT, confidence REAL)''')
    conn.commit()
    conn.close()

def save_mood(emotion, confidence):
    conn = sqlite3.connect('mood_history.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO moods (timestamp, emotion, confidence) VALUES (?, ?, ?)",
              (timestamp, emotion, confidence))
    conn.commit()
    conn.close()

def get_mood_history(days=7):
    conn = sqlite3.connect('mood_history.db')
    c = conn.cursor()
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
    c.execute("SELECT timestamp, emotion, confidence FROM moods WHERE timestamp > ? ORDER BY timestamp DESC", (cutoff,))
    history = c.fetchall()
    conn.close()
    return history

# ====================== CORE FUNCTIONS ======================
def detect_emotion(frame):
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = DeepFace.analyze(
            img_path=rgb_frame,
            actions=['emotion'],
            enforce_detection=False,
            silent=True,
            detector_backend="opencv"
        )
        if isinstance(result, list):
            result = result[0]
        
        emotion = result['dominant_emotion']
        confidence = result['emotion'][emotion]
        return emotion, confidence
    except Exception:
        return "neutral", 0.0

def get_spotify_recommendations(emotion, limit=5):
    try:
        mapping = EMOTION_MAPPING.get(emotion.lower(), EMOTION_MAPPING["neutral"])
        
        recs = sp.recommendations(
            seed_genres=["pop", "indie", "electronic"],
            target_valence=(mapping["valence"][0] + mapping["valence"][1]) / 2,
            min_valence=mapping["valence"][0],
            max_valence=mapping["valence"][1],
            target_energy=(mapping["energy"][0] + mapping["energy"][1]) / 2,
            min_energy=mapping["energy"][0],
            max_energy=mapping["energy"][1],
            target_tempo=(mapping["tempo"][0] + mapping["tempo"][1]) / 2,
            min_tempo=mapping["tempo"][0],
            max_tempo=mapping["tempo"][1],
            limit=limit
        )
        
        tracks = []
        for track in recs['tracks']:
            tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track.get('preview_url'),
                'spotify_url': track['external_urls']['spotify']
            })
        return tracks
    except Exception as e:
        st.error(f"Spotify API error: {e}")
        return []

# ====================== STREAMLIT APP ======================
init_db()

st.set_page_config(page_title="Mood Music", page_icon="🎵", layout="wide")
st.title("🎵 Emotion-Aware Music Recommender")
st.markdown("**Your face chooses the playlist**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Webcam")
    frame_placeholder = st.empty()

with col2:
    emotion_placeholder = st.empty()
    recommendations_placeholder = st.empty()

# Controls
if st.button("🚀 Detect My Mood & Get Music", type="primary", use_container_width=True):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Cannot access webcam. Please allow camera permission.")
    else:
        st.info("🔍 Analyzing your emotion... (stay in front of camera)")
        start_time = time.time()
        detected_emotion = None
        confidence = 0.0

        while time.time() - start_time < 15:  # Max 15 seconds
            ret, frame = cap.read()
            if not ret:
                break

            # Show live feed
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(rgb_frame, channels="RGB", use_column_width=True)

            # Detect periodically
            if int(time.time() - start_time) % 2 == 0:
                emotion, conf = detect_emotion(frame)
                if conf > 60.0:
                    detected_emotion = emotion
                    confidence = conf
                    break
                else:
                    emotion_placeholder.info(f"Detected: **{emotion}** ({conf:.1f}%) — Waiting for stronger signal...")

        cap.release()

        if detected_emotion:
            emotion_placeholder.success(f"✅ Detected: **{detected_emotion.capitalize()}** ({confidence:.1f}%)")
            save_mood(detected_emotion, confidence)

            with st.spinner("Fetching Spotify recommendations..."):
                tracks = get_spotify_recommendations(detected_emotion)

            if tracks:
                recommendations_placeholder.subheader("🎧 Recommended Tracks")
                for track in tracks:
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if track['album_art']:
                            st.image(track['album_art'], width=110)
                    with c2:
                        st.write(f"**{track['name']}**")
                        st.caption(f"by {track['artist']}")
                        if track['preview_url']:
                            st.audio(track['preview_url'], format="audio/mp3")
                        st.markdown(f"[Open on Spotify]({track['spotify_url']})")
                    st.divider()
            else:
                st.warning("No tracks found. Try again.")
        else:
            emotion_placeholder.warning("⚠️ Could not detect face with high confidence. Using Neutral mood.")
            tracks = get_spotify_recommendations("neutral")
            # Display tracks similarly...

# History
st.subheader("📅 Mood History (Last 7 Days)")
history = get_mood_history()
if history:
    for ts, emo, conf in history[:10]:
        date = ts.split("T")[0]
        st.write(f"**{date}** → {emo.capitalize()} ({conf:.1f}%)" )
else:
    st.info("No history yet. Detect your mood to start tracking!")