from fastapi import FastAPI
from app.routers import predict

app = FastAPI()

app.include_router(predict.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de predicción de F1"}