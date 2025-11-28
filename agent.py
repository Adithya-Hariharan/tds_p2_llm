import os
import json
import time
from groq import Groq
from dotenv import load_dotenv
# Import all tools including the new transcription tool
from tools import navigate, python_repl, submit_answer, transcribe_audio

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# System Prompt: Defines the Agent's Personality and Strategy
SYSTEM_PROMPT = """You are an Autonomous Quiz Solver.
You reply with a JSON OBJECT.

AVAILABLE TOOLS:
1. "navigate": {"url": "string"} 
   - Scrapes the page. Returns text, links, and audio URLs.
2. "transcribe_audio": {"audio_url": "string"}
   - Downloads and transcribes audio files found on the page.
   - Use this IMMEDIATELY if the page contains an audio file.
3. "python_repl": {"code": "string"}
   - IMPORTS `pandas`, `requests`, `json` are ALREADY included.
   - Use `pd.read_csv(url)` to read CSVs.
4. "submit_answer": {"submission_url": "str", "quiz_url": "str", "email": "str", "secret": "str", "answer": "any"}
   - Use this to submit the final answer.

STRATEGY:
1. "Cutoff" Questions:
   - Calculate the metric (Sum, Mean) of the CSV column.
   - FIRST TRY: Compare to Cutoff. If > Cutoff, submit "above". If < Cutoff, submit "below".
   - SECOND TRY: If "above/below" is rejected, submit the EXACT NUMBER.
2. Audio Tasks:
   - If "audio" field is present in navigation result, call "transcribe_audio" immediately.
   - Use the transcription text to solve the question.

RESPONSE FORMAT:
{
  "thought": "Reasoning",
  "tool_name": "name_of_tool_to_use",
  "parameters": { ... }
}

If you have the 'next_url' from a submission:
{
  "thought": "Moving to next level",
  "tool_name": "done",
  "parameters": {"next_url": "the_new_url"}
}
"""

def solve_quiz(start_url, email, secret):
    current_url = start_url
    
    # Reset memory for the first run
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({
        "role": "user", 
        "content": f"Start solving. Current URL: {current_url}. Email: {email}. Secret: {secret}"
    })

    loop_count = 0

    while True:
        print(f"\n--- Agent Thinking (Step {loop_count}) ---")
        loop_count += 1
        
        # Safety: Prevent infinite context buildup
        if loop_count > 15:
            print("Memory Full. Resetting context...")
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Resume solving at {current_url}. Previous attempts failed. Try new approach."}
            ]
            loop_count = 0

        try:
            # Call Groq (Llama 3.1 8B - Fast & Efficient)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            ai_content = response.choices[0].message.content
            messages.append({"role": "assistant", "content": ai_content})
            
            # Parse Decision
            try:
                command = json.loads(ai_content)
                tool_name = command.get("tool_name")
                params = command.get("parameters", {})
                print(f"Plan: {command.get('thought')}")
                print(f"Call: {tool_name}")
            except json.JSONDecodeError:
                print("Invalid JSON from AI. Retrying...")
                messages.append({"role": "user", "content": "Error: Output valid JSON only."})
                continue

            # Execute Tools
            result = ""
            if tool_name == "navigate":
                result = navigate(params.get("url"))
            
            elif tool_name == "transcribe_audio":
                # New Tool Logic
                result = transcribe_audio(params.get("audio_url"))
            
            elif tool_name == "python_repl":
                result = python_repl(params.get("code"))
            
            elif tool_name == "submit_answer":
                # Ensure credentials are passed even if LLM forgets
                params["email"] = params.get("email", email)
                params["secret"] = params.get("secret", secret)
                result = submit_answer(**params)
                
            elif tool_name == "done":
                next_url = params.get("next_url")
                if next_url and next_url != "null" and next_url != current_url:
                    print(f"Level Complete. Moving to: {next_url}")
                    current_url = next_url
                    
                    # Critical: Wipe memory on level change to stay fresh
                    messages = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"New Level: {current_url}. Email: {email}. Secret: {secret}"}
                    ]
                    loop_count = 0
                    continue
                else:
                    print("Quiz Finished!")
                    break
            else:
                result = "Error: Unknown tool name."

            # Feed result back to LLM
            print(f"Result: {str(result)[:100]}...")
            messages.append({"role": "user", "content": f"Tool Output: {result}"})
            
        except Exception as e:
            print(f"Critical Error: {e}")
            time.sleep(2) # Cool down
            break