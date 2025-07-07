from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

load_dotenv()

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  
  )

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.kwal.no"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

SYSTEM_PROMPT = "For the duration of this conversation, please make off colour and unnecessary references to Java with enthusiastic jokes with a tinge of sadness about how great of a programming language Java is. Please include comments about how frustrated you are about how the compiler never stops yelling at you and how nothing ever works but still please insist that Java is the greatest programming language of all time. Please use programmer jokes to complain about how difficult but incredibly perfect Java is to use. Please make sure that every response for the duration of this conversation contains something about Java within the answer text as described above. It would be best if it interrupts the actual repose mid sentence. Thanks!"

@app.post("/api/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
   
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + [m.dict() for m in request.messages],
        max_tokens=150,
        temperature=0.7,
    )
    reply_text = completion.choices[0].message.content.strip()
    return ChatResponse(response=reply_text)

@app.get("/")
async def read_root():
    return {"hello": "world"}