from pydantic import BaseModel

class InputData(BaseModel):
    Circuito: object
    ConstructorID: object
    Piloto: object
    Resultado_Clasificacion: float
    Promedio_Quali: float
    Promedio_posicion_circuito: float
    Tasa_podios: float