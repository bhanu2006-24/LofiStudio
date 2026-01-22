import streamlit as st
import os
import time
from audio_generator import generate_lofi_track
from utils import fetch_image, create_video

# Page configuration
st.set_page_config(
    page_title="LoFi Studio",
    page_icon="🎧",
    layout="centered"
)

# Custom CSS for aesthetics
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #ff4b4b, #ff9068);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stSelectbox, .stSlider {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.title("🎧 LoFi Studio")
st.markdown("### Generate Your Own Chill Tracks")
st.markdown("Create custom lo-fi music with visuals in seconds. Select your vibe, set the duration, and let the AI do the rest.")

# Sidebar Controls
with st.sidebar:
    st.header("Studio Controls")
    
    music_type = st.selectbox(
        "Select Vibe",
        ["Lo-Fi Beats", "Piano", "Ambient", "Synth"],
        index=0
    )
    
    track_length = st.slider(
        "Track Length (seconds)",
        min_value=30,
        max_value=600, # 10 minutes
        value=60,
        step=10
    )

    st.markdown("---")
    st.markdown("Powered by **LoFi Studio Engine**")

# Main Content Area
col1, col2 = st.columns([1, 2])

# Placeholder for content
if 'generated' not in st.session_state:
    st.session_state.generated = False

def generate_content():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. Generate Audio
    status_text.text("🎹 Composing melody...")
    try:
        audio_file = generate_lofi_track(track_length, music_type)
        st.session_state.audio_path = audio_file
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return
    progress_bar.progress(30)
    
    # 2. Fetch Image
    status_text.text("🎨 Painting the scene...")
    prompt_map = {
        "Lo-Fi Beats": "lofi anime study girl room night cozy window rain",
        "Piano": "melancholic fantasy landscape river sunset",
        "Ambient": "space nebula cosmic ethereal abstract",
        "Synth": "cyberpunk city neon rain night futuristic"
    }
    image_prompt = prompt_map.get(music_type, "lofi cozy aesthetics")
    
    try:
        image_file = fetch_image(image_prompt)
        st.session_state.image_path = image_file
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        return
    progress_bar.progress(60)
    
    # 3. Render Video
    status_text.text("🎬 Rendering video final cut...")
    try:
        video_file = create_video(st.session_state.audio_path, st.session_state.image_path, "lofi_studio_output.mp4")
        st.session_state.video_path = video_file
    except Exception as e:
        st.error(f"Error rendering video: {e}")
        return
    progress_bar.progress(100)
    
    status_text.text("✨ Creation Complete!")
    st.session_state.generated = True
    time.sleep(1)
    status_text.empty()
    progress_bar.empty()

# Generate Button
if st.button("Generate Track", use_container_width=True):
    with st.spinner("Entering the studio..."):
        generate_content()

# Display Results
if st.session_state.generated:
    st.markdown("---")
    
    # Show Visuals
    if os.path.exists(st.session_state.image_path):
        st.image(st.session_state.image_path, caption=f"Vibe: {music_type}", use_column_width=True)
    
    # Audio Player
    if os.path.exists(st.session_state.audio_path):
        st.markdown("#### 🎧 Preview Audio")
        st.audio(st.session_state.audio_path)
        
        with open(st.session_state.audio_path, "rb") as f:
            st.download_button(
                label="Download Audio (MP3/WAV)",
                data=f,
                file_name=f"lofi_studio_{music_type.lower().replace(' ', '_')}.wav",
                mime="audio/wav"
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
