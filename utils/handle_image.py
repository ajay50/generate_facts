import time

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

def download_image_from_gemini(output_path, prompt, api_key ):

    # --- Initialize the Client ---
    client = genai.Client(api_key=api_key)
    print(f"Downloading {prompt}...")
    print(f"output_path {output_path}...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
          response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
      if part.text is not None:
        print(part.text)
      elif part.inline_data is not None:
        image = Image.open(BytesIO((part.inline_data.data)))
        image.save(output_path)
        filename = f"content/images/img_{int(time.time())}.png"
        image.save(filename)
        print(f"Writing image to {output_path}")

def download_image_from_gemini1(output_path, prompt, api_key):
    # --- Initialize the Client ---
    client = genai.Client(api_key=api_key)
    print(f"Downloading {prompt}...")
    print(f"output_path {output_path}...")
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(output_path)
            print(f"✅ Saved: {output_path}")
            return output_path
    return "images/default.jpg"