from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    text: str


class ChatResponse(BaseModel):
    audio_url: str = Field(..., alias="audioUrl")
    text: str
