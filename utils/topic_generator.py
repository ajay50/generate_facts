# utils/topic_generator.py

import google.generativeai as genai

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def generate_viral_topic(model, broad_topic):
    prompt = f"""
You are a viral content strategist for YouTube Shorts.

Take the following broad topic and turn it into a viral micro-topic.
The micro-topic must:
- Trigger curiosity or emotion (e.g. fear, surprise, amazement)
- Be short (under 12 words)
- Sound like a fact for a YouTube Short
- Avoid generic phrases. Be specific, weird, or shocking.

Respond with only one line. No extra words.

Topic: {broad_topic}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
