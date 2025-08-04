# utils/video_creator.py
import random
import time

from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.editor import *
from PIL import Image

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


def create_video(image_path, audio_folder, out_path):
    print(f"Creating video from image  {image_path}")
    print(f"Creating video from audio  {audio_folder}")
    print(f"Creating video from output {out_path}")
    print("🎬 Creating video...")
    clip = ImageClip(image_path).set_duration(6)
    music_path = pick_random_music(audio_folder)
    bg_music = AudioFileClip(music_path)
    looped = audio_loop(bg_music, duration=6).volumex(0.2)
    final = clip.set_audio(looped)
    os.makedirs("content/video", exist_ok=True)
    # Write final video
    final.write_videofile(out_path, fps=30, codec="libx264")
    return out_path

def pick_random_music(MUSIC_DIR):
    files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3") and is_valid_mp3(os.path.join(MUSIC_DIR, f))]
    if not files:
        raise RuntimeError("❌ No valid background music found.")
    return os.path.join(MUSIC_DIR, random.choice(files))

def is_valid_mp3(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(3)
            return header == b'ID3' or file_path.endswith('.mp3') and os.path.getsize(file_path) > 1024
    except:
        return False
