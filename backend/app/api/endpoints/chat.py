from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_service import chat_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history_id: str = None

@router.post("/")
async def chat(request: ChatRequest):
    response_data = await chat_service.get_response(request.message)
    return {
        "response": response_data["response"],
        "sources": list(set(response_data["sources"]))
    }
