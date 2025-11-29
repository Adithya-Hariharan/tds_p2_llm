# Save as test_project2.py
import requests
NGROK_URL = "https://adelaide-glyptic-windily.ngrok-free.dev/quiz"
PROJECT2_URL = "https://tds-llm-analysis.s-anand.net/project2"  # ← THIS

payload = {"email": "student@example.com", "secret": "TDS-SECRET-KEY-99", "url": PROJECT2_URL}
print(f"Sending test request to {NGROK_URL}...")
try:
    response = requests.post(NGROK_URL, json=payload)
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    print(f"Error: {e}")