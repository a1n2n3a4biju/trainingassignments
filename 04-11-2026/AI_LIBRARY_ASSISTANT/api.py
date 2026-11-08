
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Library AI Assistant API is running"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = run_agent(request.message)

    return {
        "response": response
    }
