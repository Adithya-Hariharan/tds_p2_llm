import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_url: str) -> str:
    """
    Downloads audio from a URL and transcribes it using Groq's Whisper model.
    """
    print(f"[Tool] Transcribing: {audio_url}")

    if not audio_url.startswith(("http://", "https://")):
        audio_url = "https://tds-llm-analysis.s-anand.net" + audio_url
        print(f"[Tool] Fixed to full URL: {audio_url}")
    temp_filename = "temp_audio_file"
    
    try:
        # 1. Download the audio file
        response = requests.get(audio_url, stream=True)
        if response.status_code != 200:
            return f"Error: Failed to download audio (Status {response.status_code})"
        
        if len(response.content) < 100:
             return f"Error: Downloaded file is too small. It might not be audio."
        # Groq supports these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
        # We try to detect extension or default to .mp3
        if ".ogg" in audio_url: ext = ".ogg"
        elif ".wav" in audio_url: ext = ".wav"
        else: ext = ".mp3"
        
        filename = f"{temp_filename}{ext}"
        
        with open(filename, "wb") as f:
            f.write(response.content)
            
        # 2. Send to Groq for Transcription
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(filename, file.read()),
                model="whisper-large-v3",
                response_format="json",
                language="en",
                temperature=0.0
            )
            
        # 3. Cleanup
        if os.path.exists(filename):
            os.remove(filename)
            
        return f"TRANSCRIPTION: {transcription.text}"

    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        return f"Transcription Error: {e}"