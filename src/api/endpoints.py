# src/api/endpoints.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.model import MedicalChatbot

router = APIRouter()
chatbot = MedicalChatbot()

class QueryRequest(BaseModel):
    query: str
    history: list[list[str]] = []

class QueryResponse(BaseModel):
    response: str
    history: list[list[str]]

@router.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Only keep the last 4 rounds of conversation
    clipped_history = request.history[-4:] if request.history else []

    response = chatbot.get_response(request.query, conversation_history=clipped_history)
    updated_history = clipped_history + [[request.query, response]]

    return QueryResponse(response=response, history=updated_history)

