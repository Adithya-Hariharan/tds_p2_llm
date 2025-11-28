import uvicorn
import os
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import solve_quiz

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verify this matches your Google Form submission
MY_SECRET_KEY = os.getenv("QUIZ_SECRET", "TDS-SECRET-KEY-99") 

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str

async def run_agent_task(url: str, email: str, secret: str):
    """Runs the agent in the background."""
    print(f"Background: Starting agent for {url}")
    await asyncio.to_thread(solve_quiz, url, email, secret)

@app.post("/quiz")
async def quiz_endpoint(request: QuizRequest, background_tasks: BackgroundTasks):
    print(f"Received Request: {request}")
    
    # 1. Security Check
    if request.secret != MY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid secret provided.")
    
    # 2. Start Agent
    background_tasks.add_task(run_agent_task, request.url, request.email, request.secret)
    
    return {"message": "Quiz task accepted. Agent started.", "status": "processing"}

@app.get("/")
def read_root():
    return {"status": "alive", "service": "LLM Quiz Solver"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)