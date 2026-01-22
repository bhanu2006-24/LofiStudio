import requests
import shutil
from moviepy.editor import AudioFileClip, ImageClip
import os

def fetch_image(prompt, width=1280, height=720, output_filename="assets/generated/background_image.jpg"):
    safe_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&nologo=true"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    response = requests.get(url, stream=True, timeout=10)
    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return output_filename
    else:
        raise Exception(f"Failed to fetch image. Status: {response.status_code}")

def create_video(audio_path, image_path, output_path="assets/generated/output_video.mp4"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio = AudioFileClip(audio_path)
    video = ImageClip(image_path).set_duration(audio.duration)
    video = video.set_audio(audio)
    # Use simple codec to ensure compatibility
    video.write_videofile(output_path, fps=1, codec="libx264", audio_codec="aac")
    return output_path

def convert_wav_to_mp3(wav_path, output_path="assets/generated/output_audio.mp3"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio = AudioFileClip(wav_path)
    audio.write_audiofile(output_path, codec='mp3')
    return output_path
