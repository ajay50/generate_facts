# utils/image_creator.py
from io import BytesIO

from PIL import Image
import google.generativeai as genai
from google.genai import types

from youtube_bot.utils.handle_image import download_image_from_gemini


def create_image_prompt_with_gemini(text, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    system_prompt = f"""
write prompt create Create realistic image for youtube short and add attractive text in image: \"{text}\" with like and subscribe icon. great prompt. 9 to 6 ratio image. only prompt in response
"""
    response = model.generate_content(system_prompt)
    return response.text.strip()



def generate_image_with_text(text, gemini_key, out_path="content/images/final.png"):
    # Step 1: Use Gemini to generate visual prompt
    visual_prompt = create_image_prompt_with_gemini(text, gemini_key)
    print("[Gemini Visual Prompt]:", visual_prompt)

    # Step 2: Generate image with DALL·E
    download_image_from_gemini(out_path, visual_prompt, gemini_key)

    return out_path
