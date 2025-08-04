from google import genai
from google.genai import types
from PIL import Image, UnidentifiedImageError  # Import UnidentifiedImageError specifically
from io import BytesIO
import base64
import os

# --- Configuration ---
API_KEY = "AIzaSyAhP32bypLzyLtf7nBAr8yUbbnelow-VCw"  # <<<<< REPLACE WITH YOUR ACTUAL API KEY
# API_KEY = os.getenv("GEMINI_API_KEY") # Recommended for production

# --- Initialize the Client ---
client = genai.Client(api_key=API_KEY)

contents = ('A breathtaking, futuristic digital illustration representing Generative AI. Imagine a luminous, swirling vortex of interconnected data streams and shimmering algorithmic patterns, radiating outwards from a central, ethereal core. From this dynamic nexus, abstract, vibrant forms are gracefully emerging and taking shape – hints of evolving organic fractals, intricate digital architectures, or fantastical abstract landscapes.'
'The color palette is a symphony of electric blues, radiant purples, vibrant fuchsias, and pulsating neon greens, all bathed in an iridescent, glowing light. Visual metaphors include a digital \'big bang\' of creativity, a flowing river of innovation, and light particles coalescing into new realities.'
'The style is high-tech, fluid, and ethereal, with a strong sense of movement and infinite possibility. Volumetric lighting should emphasize depth and glow. The emotional tone is one of awe, wonder, innovation, and boundless creativity. It should feel dynamic and visually arresting, perfect as a background that suggests constant evolution and groundbreaking ideas.'
'*   **Visual Style:** Futuristic digital art, abstract, conceptual, luminous, glowing, vibrant gradients, fluid lines, high detail.'
'*   **Colors:** Electric blue, radiant purple, fuchsia, neon green, teal, hints of gold/silver iridescence.'
'*   **Composition:** Central focus with energy radiating outwards, sense of depth and infinite space. Not too busy, leaving room for text overlays.'
'*   **Emotional Tone:** Awe, wonder, excitement, inspiration, innovation, optimism.'
'*   **Keywords:** Generative AI, AI creation, digital art, neural networks, data visualization, algorithmic art, futuristic, sci-fi, cosmic, abstract' 'expressionism, luminous, ethereal, dynamic, ultra HD, 8k, conceptual art, ArtStation trend, cinematic lighting.')

# Ensure the model name is correct for image generation.
model_name = "gemini-2.0-flash-preview-image-generation"  # Use a variable for clarity

# Create an output directory if it doesn't exist
output_dir = "generated_images"
os.makedirs(output_dir, exist_ok=True)

try:
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    image_generated = False  # Flag to check if an image was successfully processed
    print(f" Response: {response}")
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        for i, part in enumerate(response.candidates[0].content.parts):
            print(f"\nProcessing Part {i + 1}:")
            if part.text is not None:
                print(f"  Text Part: {part.text[:200]}...")
            elif part.inline_data is not None:
                image_base64_data = part.inline_data.data
                mime_type = part.inline_data.mime_type

                print(f"  Found Inline Data with MIME type: {mime_type}")
                print(f"  Raw base64 data length: {len(image_base64_data)}")
                print(f"  Raw base64 data (first 100 chars): {image_base64_data[:100]}...")

                if isinstance(image_base64_data, str) and image_base64_data.startswith('data:'):
                    if ',' in image_base64_data:
                        image_base64_data = image_base64_data.split(',')[1]
                        print("  Stripped 'data:image/...' prefix.")
                    else:
                        print("  ⚠️ Warning: Base64 data starts with 'data:' but no comma found. Proceeding as-is.")

                try:
                    image_bytes = base64.b64decode(image_base64_data)

                    if not image_bytes:
                        print("  ❌ Decoded image data is EMPTY. Skipping this part.")
                        continue

                    print(f"  Decoded image bytes length: {len(image_bytes)}")

                    # This is where Pillow will now be more tolerant of truncation
                    image = Image.open(BytesIO(image_bytes))

                    image = image.convert("RGB")

                    # Optional: Resize image
                    # image = image.resize((720, 1280), Image.LANCZOS)
                    OUTPUT_DIR = 'generated_images'
                    output_filename = f"gemini-native-image_{i + 1}.png"
                    output_path = os.path.join(OUTPUT_DIR, output_filename)
                    image.save(output_path)
                    print(f"  ✅ Image successfully saved to: {output_path}")
                    image.show()
                    image_generated = True
                    # break # Uncomment if you only want the first image

                except (base64.binascii.Error) as e:
                    print(f"  ❌ Base64 decoding error for this part: {e}")
                except UnidentifiedImageError as e:
                    print(f"  ❌ PIL.UnidentifiedImageError (even with LOAD_TRUNCATED_IMAGES=True): {e}")
                    print("  This indicates severe corruption or extremely short data.")
                    debug_bytes_path = os.path.join(OUTPUT_DIR, f"debug_bytes_part_{i + 1}.bin")
                    with open(debug_bytes_path, "wb") as f:
                        f.write(image_bytes)
                    print(f"  Raw decoded bytes saved to {debug_bytes_path} for manual inspection.")
                except Exception as e:
                    print(f"  ❌ An unexpected error occurred during image processing for Part {i + 1}: {e}")
            else:
                print("  Part contains no text or inline_data.")
    else:
        print("❌ Response contains no candidates or content parts.")
    if not image_generated:
        print("\n⚠️ No identifiable image was successfully generated and processed from the API response.")
        print(f"Full response received: {response.text}")  # Print the whole text for detailed debugging

except genai.types.BlockedPromptException as e:
    print(f"❌ Prompt was blocked due to safety concerns: {e}")
except Exception as e:
    print(f"❌ Gemini AI image generation failed at API call level: {e}")
