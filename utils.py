import requests
import shutil
from moviepy.editor import AudioFileClip, ImageClip
import os

def fetch_image(prompt, width=1280, height=720):
    safe_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&nologo=true"
    filename = "background_image.jpg"
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return filename
    except Exception as e:
        print(f"Error fetching image: {e}")
    return None

def create_video(audio_path, image_path, output_path="output_video.mp4"):
    try:
        audio = AudioFileClip(audio_path)
        video = ImageClip(image_path).set_duration(audio.duration)
        video = video.set_audio(audio)
        # Use simple codec to ensure compatibility
        video.write_videofile(output_path, fps=1, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        print(f"Error creating video: {e}")
        return None

def convert_wav_to_mp3(wav_path, output_path="output_audio.mp3"):
    try:
        audio = AudioFileClip(wav_path)
        audio.write_audiofile(output_path, codec='mp3')
        return output_path
    except Exception as e:
        print(f"Error converting audio: {e}")
        return None
