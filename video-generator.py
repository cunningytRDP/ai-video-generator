from flask import Flask, request, jsonify
from moviepy.editor import *
import requests
import os

app = Flask(__name__)

@app.route('/video-generate', methods=['POST'])
def generate_video():
    data = request.json
    audio_url = data['audio_url']
    image_url = data['image_url']
    filename = data.get('output_filename', 'ai_news_video.mp4')

    # Download audio
    audio_path = 'voice.mp3'
    with open(audio_path, 'wb') as f:
        f.write(requests.get(audio_url).content)

    # Download image
    image_path = 'background.jpg'
    with open(image_path, 'wb') as f:
        f.write(requests.get(image_url).content)

    # Create video using MoviePy
    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).set_duration(audio.duration).set_audio(audio).resize(height=720)
    image.write_videofile(filename, fps=24)

    return jsonify({"status": "success", "video_url": f"https://yourdomain.com/{filename}"})
