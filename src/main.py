from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import base_router, service_router


# Инициализация FastAPI
app = FastAPI(title='apischool', docs_url='/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://0.0.0.0:8000",
        "http://127.0.0.1:8000"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Подключение роутеров
app.include_router(base_router)
app.include_router(service_router)
