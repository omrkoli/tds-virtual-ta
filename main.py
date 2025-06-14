from fastapi import FastAPI
from pydantic import BaseModel
import json

# Define the structure of the request
class QuestionRequest(BaseModel):
    question: str
    image: str = None

# Create the FastAPI app
app = FastAPI()

# Load your FAQ data from JSON
with open("data/tds_faq.json", "r") as file:
    faq_data = json.load(file)

# Define your route
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

