from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://f1-ai-front.onrender.com"],  # URL de tu app React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)