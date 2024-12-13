from fastapi import APIRouter
from app.schemas.input_data import InputData
from app.models.ann_model import predict_podium

router = APIRouter()

@router.post("/predict")
def get_prediction(input_data: InputData):
    prediction = predict_podium(input_data)
    return {"podio": prediction}