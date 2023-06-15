from pydantic import BaseModel, Field


class HintRequest(BaseModel):
    riddle_num: int = Field(..., alias="riddleNum")
    hint_num: int = Field(..., alias="hintNum")


class ChatResponse(BaseModel):
    audio_url: str = Field(..., alias="audioUrl")
    text: str
    ai_text: str = Field(..., alias="aiText")
