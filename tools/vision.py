import os
import base64
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(image_url):
    """Downloads an image and converts it to base64 string."""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        else:
            return None
    except Exception:
        return None

def analyze_image(image_url: str, question: str = "What is in this image?") -> str:
    """
    Analyzes an image using Groq's Vision model.
    """
    print(f"[Tool] Analyzing Image: {image_url}")
    
    base64_image = encode_image(image_url)
    if not base64_image:
        return "Error: Could not download image."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
            temperature=0.1,
        )
        
        result = chat_completion.choices[0].message.content
        return f"IMAGE ANALYSIS: {result}"

    except Exception as e:
        return f"Vision Error: {str(e)}"