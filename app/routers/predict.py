from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.schemas.input_data import InputData
from app.models.ann_model import predict_podium

router = APIRouter()

@router.post("/predict")
def get_prediction(input_data: InputData):
    try:
        # Intentamos hacer la predicción con los datos
        prediction = predict_podium(input_data)
        return {"podio": prediction}
    
    except ValidationError as e:
        # En caso de error de validación, capturamos los campos incorrectos
        errors = []
        for error in e.errors():
            field_name = error.get("loc")[0]  # El nombre del campo con el error
            error_msg = error.get("msg")  # Mensaje de error
            errors.append(f"Campo '{field_name}' tiene un error: {error_msg}")
        
        # Devolvemos los errores de manera personalizada
        raise HTTPException(status_code=422, detail=errors)
