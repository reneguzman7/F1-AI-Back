from pydantic import BaseModel

class InputData(BaseModel):
    circuito: float
    constructor_id: float
    piloto: float
    resultado_clasificacion: float
    promedio_quali: float
    promedio_posicion_circuito: float
    tasa_podios: float