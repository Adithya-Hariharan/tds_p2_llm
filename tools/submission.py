import requests
import json

def submit_answer(submission_url: str, quiz_url: str, email: str, secret: str, answer: str) -> str:
    """
    POSTs the answer to the server.
    Returns the server's JSON response (which often contains the next URL).
    """
    print(f" [Tool] Submitting to {submission_url} | Answer: {answer}")
    try:
        payload = {
            "email": email,
            "secret": secret,
            "url": quiz_url,
            "answer": answer
        }
        # 15s timeout to prevent hanging
        resp = requests.post(submission_url, json=payload, timeout=15)
        
        # Return JSON if possible, else text
        try:
            return json.dumps(resp.json())
        except:
            return resp.text
            
    except Exception as e:
        return f"Submission Error: {e}"