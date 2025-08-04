# utils/text_generator.py
import google.generativeai as genai
import random

from youtube_bot.utils.topic_generator import generate_viral_topic


def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def load_prompts(file_path="prompts/prompts.txt"):
    with open(file_path) as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def generate_text(model, topic, prompts):
    viral_topic = generate_viral_topic(model, topic)
    print("🎯 Viral Micro-Topic:", viral_topic)
    selected = random.sample(prompts, 1)
    combined_result = []
    #for prompt in selected:
   #     full_prompt = f"{prompt}\nTopic: {viral_topic}"
   #     response = model.generate_content(full_prompt)
   #     combined_result.append(response.text.strip())
    return "\n".join(viral_topic)

# utils/text_generator.py

import google.generativeai as genai

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def generate_hook_and_fact(model, topic):
    prompt = f"""
You are a viral Shorts script writer.

Task:
1. Create a HOOK — one short, curiosity-triggering sentence. No emojis.
2. Create a FACT — one short, shocking or amazing fact with 1–2 emojis.

Make both simple, 1 line each. Keep it informal and engaging.

Respond in this format only:
Hook: <one line>
Fact: <one line with emojis>

Topic: {topic}
"""

    response = model.generate_content(prompt)
    return response.text.strip()

