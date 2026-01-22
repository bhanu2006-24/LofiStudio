from utils import convert_wav_to_mp3, fetch_image
from audio_generator import generate_lofi_track
import os

def debug_step_by_step():
    print("--- 1. Generating WAV ---")
    try:
        wav_path = generate_lofi_track(5, "Lo-Fi Beats")
        print(f"WAV Path: {wav_path}")
        if os.path.exists(wav_path):
            print(f"WAV File Size: {os.path.getsize(wav_path)} bytes")
        else:
            print("WAV file NOT created.")
            return
    except Exception as e:
        print(f"WAV Generation Error: {e}")
        return

    print("\n--- 2. Converting to MP3 ---")
    try:
        mp3_path = convert_wav_to_mp3(wav_path, "debug_audio.mp3")
        print(f"MP3 Path (result): {mp3_path}")
        if mp3_path and os.path.exists(mp3_path):
            print(f"MP3 File Size: {os.path.getsize(mp3_path)} bytes")
        else:
            print("MP3 file NOT created (check moviepy/ffmpeg logs above).")
    except Exception as e:
        print(f"MP3 Conversion Exception: {e}")

    print("\n--- 3. Fetching Image ---")
    try:
        img_path = fetch_image("test prompt")
        print(f"Image Path: {img_path}")
        if img_path and os.path.exists(img_path):
             print(f"Image File Size: {os.path.getsize(img_path)} bytes")
        else:
             print("Image file NOT created.")
    except Exception as e:
        print(f"Image Fetch Exception: {e}")

if __name__ == "__main__":
    debug_step_by_step()
