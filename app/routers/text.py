from __future__ import annotations

import os

from fastapi import APIRouter

from app.models.hint import ChatResponse
from app.services.text import TextService

router = APIRouter()

os.environ["OPENAI_API_KEY"] = ""


@router.get("/api/v1/text")
async def text():
    text_service = TextService()
    text_service.process("The Author is Ros")
    # docs = text_service.search("who are the authors of the book?")
    resp = ChatResponse(
        audioUrl="https://storage.googleapis.com/test_audio_ml_pipeline/ \
        2d50d9a3-880b-4e11-8eea-a93996c8b59f.wav",
        text="Open door",
    )
    return resp

    # chain = load_qa_chain(OpenAI(),
    #                   chain_type="stuff")
    # chain.run(input_documents=docs, question="who are the authors of the book?")
    # return docs[0]
