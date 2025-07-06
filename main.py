from fastapi import FastAPI
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  
  )

class ChatRequest(BaseModel):
    user_message: str = Field(..., alias="user message")

    class Config: 
        allow_population_by_field_name = True

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.kwal.no"],
    allow_methods=["*"]
)

SYSTEM_PROMPT = "For the duration of this conversation, please make off colour and unnecessary references to Java with enthusiastic jokes with a tinge of sadness about how great of a programming language Java is. Please include comments about how frustrated you are about how the compiler never stops yelling at you and how nothing ever works but still please insist that Java is the greatest programming language of all time. Please use programmer jokes to complain about how difficult but incredibly perfect Java is to use. Please make sure that every response for the duration of this conversation contains something about Java within the answer text as described above. It would be best if it interrupts the actual repose mid sentence. Thanks!"

@app.post("/api/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
   
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.user_message}],
        max_tokens=150,
        temperature=0.7,
    )
    reply_text = completion.choices[0].message.content.strip()
    return ChatResponse(response=reply_text)
