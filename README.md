# 🎧 LoFi Studio

LoFi Studio is a Streamlit-based application that allows users to generate custom Lo-Fi tracks paired with aesthetic visuals. It's designed to prototype a workflow for creating YouTube relaxation videos or just for personal enjoyment.

## Features

- **Custom Audio Generation**: Select from different vibes like Lo-Fi Beats, Piano, Ambient, and Synth.
- **Dynamic Visuals**: Automatically fetches cozy/anime-style images matching the selected vibe.
- **Video Creation**: Renders a complete MP4 video combining the generated audio and visual.
- **Control**: Adjust track length from 30 seconds to 10 minutes.
- **Export**: easy download options for both the standalone audio (WAV) and the final video (MP4).

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/yourusername/lofi-studio.git
    cd lofi-studio
    ```

2.  Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2.  Open your browser to the local URL provided (usually `http://localhost:8501`).

3.  Use the sidebar to:
    - Select your desired music style.
    - Set the track duration.
    - Click **Generate Track**.

4.  Wait for the magic to happen, then preview and download your creations!

## Technologies

- **Streamlit**: For the interactive web UI.
- **NumPy & SciPy**: For procedural audio synthesis.
- **MoviePy**: For video rendering and compositing.
- **Pollinations AI**: For generating aesthetic background images.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
