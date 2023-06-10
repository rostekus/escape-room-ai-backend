from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.chat import router as chat_router
from app.routers.hint import router as hint_router
from app.routers.text import router as text_router
from dotenv import load_dotenv


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(hint_router)
    _app.include_router(chat_router)
    _app.include_router(text_router)
    return _app


load_dotenv()
app = get_application()
