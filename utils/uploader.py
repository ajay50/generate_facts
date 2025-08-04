# utils/uploader.py
import openai
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

import google.generativeai as genai

def generate_title_desc(script, gemini_api_key):
    import google.generativeai as genai
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a professional YouTube Shorts content strategist and SEO expert.

For the following script, generate:
1. A **highly clickable YouTube Shorts title** (under 100 characters).
2. A **10-line engaging description** with emojis, plain text, and 3-5 relevant hashtags.
3. A **list of 15 relevant viral hashtags** based on the topic (only the hashtags, no extra text).

Script:
\"\"\"{script}\"\"\"

Respond in this exact format:
Title: <your title>
Description: <your description>
Hashtags: <comma-separated list of 15 hashtags>
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini title/description generation failed:", e)
        return """Title: AI-Generated Shorts
Description: Created by Gemini
Hashtags: #Shorts, #Facts, #AI, #DidYouKnow, #FunFacts, #Viral, #YouTubeShorts, #MindBlown, #Trending, #Knowledge, #AmazingFacts, #Science, #Tech, #Educational, #Incredible"""


def get_authenticated_service():
    creds = None
    token_file = "token.pickle"
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(video_path, title, description, tags=None):
    youtube = get_authenticated_service()
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["shorts", "ai", "facts"],
            "categoryId": "22"  # 'People & Blogs' category
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    print("Uploading to YouTube...")
    response = request.execute()
    print("✅ Uploaded. Video ID:", response.get("id"))
