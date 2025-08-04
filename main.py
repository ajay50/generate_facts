import os
import random
import time
from datetime import datetime
from dotenv import load_dotenv

from utils.text_generator import init_gemini, load_prompts, generate_text, generate_hook_and_fact
from utils.image_creator import generate_image_with_text
from utils.video_creator import create_video
from utils.uploader import generate_title_desc, upload_to_youtube
from youtube_bot.utils.topic_generator import generate_viral_topic

# Setup
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USED_SCRIPTS_FILE = "prompts/used_scripts.txt"
MUSIC_FOLDER = "music"
VIDEO_OUTPUT_DIR = "content/video"

def is_script_used(script_text):
    if not os.path.exists(USED_SCRIPTS_FILE):
        return False
    with open(USED_SCRIPTS_FILE, "r", encoding="utf-8") as f:
        return script_text.strip() in f.read()

def save_script(script_text):
    with open(USED_SCRIPTS_FILE, "a", encoding="utf-8") as f:
        f.write(script_text.strip() + "\n---\n")

def run_once():
    # Load topics
    with open("prompts/topic.txt") as f:
        topics = [line.strip() for line in f if line.strip()]
        random.shuffle(topics)

    model = init_gemini(GEMINI_API_KEY)
    prompts = load_prompts()

    script = None
    max_scripts_per_topic = 10

    for topic in topics:
        print(f"\n🔍 Trying topic: {topic}")
        for attempt in range(max_scripts_per_topic):
            print(f"   ▶️ Attempt {attempt + 1}/{max_scripts_per_topic}")
            candidate_script = generate_viral_topic(model, topic)

            if not is_script_used(candidate_script):
                script = candidate_script
                save_script(script)
                print("✅ Unique script found!")
                break
            else:
                print("⚠️ Script already used. Retrying with same topic...")

        if script:
            break

    if not script:
        raise Exception("❌ No unique script found. Add new topics or improve prompts.")

    print("✅ Final Script:\n", script)

    # Generate image
    img_path = generate_image_with_text(script, GEMINI_API_KEY)

    # Create video
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"{VIDEO_OUTPUT_DIR}/video_{timestamp}.mp4"
    output_path = create_video(img_path, MUSIC_FOLDER, out_path)

    # Generate metadata
    meta = generate_title_desc(script, GEMINI_API_KEY)

    # Parse output
    try:
        title = meta.split("Title:")[1].split("Description:")[0].strip()
        description = meta.split("Description:")[1].split("Hashtags:")[0].strip()
        hashtags = meta.split("Hashtags:")[1].strip().split(",")
        hashtags = [tag.strip() for tag in hashtags if tag.strip().startswith("#")]

        # Add top 3 hashtags to the title
        title_with_hashtags = f"{title}"

        print("\n🎯 YouTube Metadata:")
        print("Title:", title_with_hashtags)
        print("Description:", description)
        print("Hashtags:", hashtags)

        # Upload
        upload_to_youtube(output_path, title_with_hashtags, description, tags=hashtags)

    except Exception as e:
        print("⚠️ Error parsing metadata:", e)
        # Fallback
        upload_to_youtube(output_path, "AI-Generated Video #Shorts", "Auto description",
                          tags=["#Shorts", "#AI", "#Facts"])


# 🔁 Run forever every 10 minutes
if __name__ == "__main__":
    run_once()