import streamlit as st
import os
import time
from audio_generator import generate_lofi_track
from utils import fetch_image, create_video, convert_wav_to_mp3

# ... (omitted shared code)

def generate_content():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. Generate Audio
    status_text.text("🎹 Composing melody...")
    try:
        wav_file = generate_lofi_track(track_length, music_type)
        # Convert to MP3
        mp3_file = convert_wav_to_mp3(wav_file, "generated_song.mp3")
        st.session_state.audio_path = mp3_file
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return
    progress_bar.progress(30)
    
    # ... (rest of the function)

# ...

    # Audio Player
    if os.path.exists(st.session_state.audio_path):
        st.markdown("#### 🎧 Preview Audio")
        st.audio(st.session_state.audio_path)
        
        with open(st.session_state.audio_path, "rb") as f:
            st.download_button(
                label="Download Audio (MP3)",
                data=f,
                file_name=f"lofi_studio_{music_type.lower().replace(' ', '_')}.mp3",
                mime="audio/mpeg"
            )

    # Video Download
    if os.path.exists(st.session_state.video_path):
        st.markdown("#### 🎬 Final Video")
        st.video(st.session_state.video_path)
        
        with open(st.session_state.video_path, "rb") as f:
            st.download_button(
                label="Download Video (MP4)",
                data=f,
                file_name=f"lofi_studio_{music_type.lower().replace(' ', '_')}.mp4",
                mime="video/mp4"
            )
