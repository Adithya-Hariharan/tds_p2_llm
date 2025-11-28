import requests

# REPLACE THIS with your actual ngrok URL from Step 4
# Example: "https://abcd-1234.ngrok-free.app/quiz"
NGROK_URL = "https://adelaide-glyptic-windily.ngrok-free.dev/quiz"

# The demo quiz URL provided in the project description
DEMO_QUIZ_URL = "https://tds-llm-analysis.s-anand.net/demo"

payload = {
    "email": "student@example.com", # Can be any email for testing
    "secret": "TDS-SECRET-KEY-99",  # MUST match what is in your .env file
    "url": DEMO_QUIZ_URL
}

print(f"Sending test request to {NGROK_URL}...")
try:
    response = requests.post(NGROK_URL, json=payload)
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    print(f"Error: {e}")