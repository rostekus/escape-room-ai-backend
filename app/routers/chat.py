from __future__ import annotations

from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.get("/")
async def index() -> dict[str, str]:
    return {
        "info": "hello" "You probably want to go to 'http://<hostname:port>/docs'.",
    }


@router.get("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(response="Hello, world!")
