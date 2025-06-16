from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

class QuestionRequest(BaseModel):
    question: str
    image: str = ""

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the FAQ data
with open("data/tds_faq.json", "r") as file:
    faq_data = json.load(file)

@app.get("/")
def root():
    return {"message": "TDS Virtual TA is running."}

@app.post("/")
def answer_question(request: QuestionRequest):
    user_question = request.question.lower()
    for item in faq_data:
        if item["question"].lower() in user_question or user_question in item["question"].lower():
            return {
                "answer": item["answer"],
                "links": [
                    {
                        "url": "https://discourse.onlinedegree.iitm.ac.in/",
                        "text": "Discourse"
                    }
                ]
            }
    return {
        "answer": f"Sorry, I don’t have an answer for: {request.question}",
        "links": []
    }
