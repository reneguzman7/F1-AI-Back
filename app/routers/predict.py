import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.schemas.input_data import InputData
from app.models.ann_model import predict_podium

router = APIRouter()

pilot_images = {
    "Lando Norris": {
        "shieldImage": "/assets/Teams/f1_2021_mclaren_logo.png",
        "pilotImage": "/assets/Drivers/lannor01.avif",
        "carImage": "/assets/Cars/mclaren.avif"
    },
    "Oscar Piastri": {
        "shieldImage": "/assets/Teams/f1_2021_mclaren_logo.png",
        "pilotImage": "/assets/Drivers/oscpia01.avif",
        "carImage": "/assets/Cars/mclaren.avif"
    },
    "Carlos Sainz Jr.": {
        "shieldImage": "/assets/Teams/f1_2021_ferrari_logo.png",
        "pilotImage": "/assets/Drivers/carsai01.avif",
        "carImage": "/assets/Cars/ferrari.avif"
    },
    "Max Verstappen": {
        "shieldImage": "/assets/Teams/f1_2021_redbull_logo.png",
        "pilotImage": "/assets/Drivers/maxver01.avif",
        "carImage": "/assets/Cars/red-bull-racing.avif"
    },
    "Pierre Gasly": {
        "shieldImage": "/assets/Teams/f1_2021_alpine_logo.png",
        "pilotImage": "/assets/Drivers/piegas01.avif",
        "carImage": "/assets/Cars/alpine.avif"
    },
    "George Russell": {
        "shieldImage": "/assets/Teams/f1_2021_mercedes_logo.png",
        "pilotImage": "/assets/Drivers/georus01.avif",
        "carImage": "/assets/Cars/mercedes.avif"
    },
    "Nico Hulkenberg": {
        "shieldImage": "/assets/Teams/f1_2021_haas_logo.png",
        "pilotImage": "/assets/Drivers/nichul01.avif",
        "carImage": "/assets/Cars/haas.avif"
    },
    "Fernando Alonso": {
        "shieldImage": "/assets/Teams/f1_2021_astonmartin_logo.png",
        "pilotImage": "/assets/Drivers/feralo01.avif",
        "carImage": "/assets/Cars/aston-martin.avif"
    },
    "Valtteri Bottas": {
        "shieldImage": "/assets/Teams/stake-f1-team-logo-wit.png",
        "pilotImage": "/assets/Drivers/valbot01.avif",
        "carImage": "/assets/Cars/kick-sauber.avif"
    },
    "Sergio Perez": {
        "shieldImage": "/assets/Teams/f1_2021_redbull_logo.png",
        "pilotImage": "/assets/Drivers/serper01.avif",
        "carImage": "/assets/Cars/red-bull-racing.avif"
    },
    "Yuki Tsunoda": {
        "shieldImage": "/assets/Teams/f1_2022_visacachapprb_logo.png",
        "pilotImage": "/assets/Drivers/yuktsu01.avif",
        "carImage": "/assets/Cars/rb.avif"
    },
    "Liam Lawson": {
        "shieldImage": "/assets/Teams/f1_2022_visacachapprb_logo.png",
        "pilotImage": "/assets/Drivers/lialaw01.avif",
        "carImage": "/assets/Cars/rb.avif"
    },
    "Lance Stroll": {
        "shieldImage": "/assets/Teams/f1_2021_astonmartin_logo.png",
        "pilotImage": "/assets/Drivers/lanstr01.avif",
        "carImage": "/assets/Cars/aston-martin.avif"
    },
    "Kevin Magnussen": {
        "shieldImage": "/assets/Teams/f1_2021_haas_logo.png",
        "pilotImage": "/assets/Drivers/kevmag01.avif",
        "carImage": "/assets/Cars/haas.avif"
    },
    "Zhou Guanyu": {
        "shieldImage": "/assets/Teams/stake-f1-team-logo-wit.png",
        "pilotImage": "/assets/Drivers/guazho01.avif",
        "carImage": "/assets/Cars/kick-sauber.avif"
    },
    "Lewis Hamilton": {
        "shieldImage": "/assets/Teams/f1_2021_mercedes_logo.png",
        "pilotImage": "/assets/Drivers/lewham01.avif",
        "carImage": "/assets/Cars/mercedes.avif"
    },
    "Jack Doohan": {
        "shieldImage": "/assets/Teams/f1_2021_alpine_logo.png",
        "pilotImage": "/assets/Drivers/jacdoo01.avif",
        "carImage": "/assets/Cars/alpine.avif"
    },
    "Alexander Albon": {
        "shieldImage": "/assets/Teams/f1_2021_williams_logo.png",
        "pilotImage": "/assets/Drivers/alealb01.avif",
        "carImage": "/assets/Cars/williams.avif"
    },
    "Charles Leclerc": {
        "shieldImage": "/assets/Teams/f1_2021_ferrari_logo.png",
        "pilotImage": "/assets/Drivers/chalec01.avif",
        "carImage": "/assets/Cars/ferrari.avif"
    },
    "Franco Colapinto": {
        "shieldImage": "/assets/Teams/f1_2021_williams_logo.png",
        "pilotImage": "/assets/Drivers/fracol01.avif",
        "carImage": "/assets/Cars/williams.avif"
    }
}

# Ruta para predecir con datos individuales
@router.post("/predict")
def get_prediction(input_data: InputData):
    try:
        # Intentamos hacer la predicciÃ³n con los datos
        prediction = predict_podium(input_data)
        return {"podio": prediction}
    
    except ValidationError as e:
        # En caso de error de validaciÃ³n, capturamos los campos incorrectos
        errors = []
        for error in e.errors():
            field_name = error.get("loc")[0]  # El nombre del campo con el error
            error_msg = error.get("msg")  # Mensaje de error
            errors.append(f"Campo '{field_name}' tiene un error: {error_msg}")
        
        # Devolvemos los errores de manera personalizada
        raise HTTPException(status_code=422, detail=errors)

# Ruta para procesar el archivo JSON y devolver resultados
@router.get("/send-data")
def send_data():
    # Ruta al archivo JSON
    file_path = os.path.join('app', 'routers', 'data.json')
    output_file_path = os.path.join('app', 'routers', 'podium-predict.json')

    try:
        # Leer el archivo JSON
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Lista para almacenar los pilotos con sus probabilidades
        pilotos_con_probabilidad = []

        # Procesar cada piloto
        for piloto in data:
            try:
                # Hacer la predicción directamente
                input_data = InputData(**piloto)
                prediction_binary, probability = predict_podium(input_data)

                # Almacenar los datos del piloto y su probabilidad
                pilotos_con_probabilidad.append({
                    "Piloto": piloto["Piloto"],
                    "Probabilidad": float(probability)  # Asegurar que es float para serialización JSON
                })

            except Exception as e:
                print(f"Error al procesar piloto {piloto.get('Piloto', 'Desconocido')}: {str(e)}")
                continue

        # Ordenar los pilotos por probabilidad (de mayor a menor)
        pilotos_ordenados = sorted(pilotos_con_probabilidad, key=lambda x: x["Probabilidad"], reverse=True)
        
        # Asignar resultados - los 3 primeros en "Podio", el resto "Fuera de podio"
        resultados = []
        for i, piloto in enumerate(pilotos_ordenados):
            resultado = "Podio" if i < 3 else "Fuera de podio"
            resultados.append({
                "Piloto": piloto["Piloto"],
                "Resultado": resultado,
                "Probabilidad": round(piloto["Probabilidad"], 4)  # Redondear a 4 decimales
            })

        # Ordenar alfabéticamente para la presentación final
        resultados_alfabeticos = sorted(resultados, key=lambda x: x["Piloto"])
        
        # Guardar los resultados en un archivo JSON
        with open(output_file_path, 'w') as output_file:
            json.dump(resultados_alfabeticos, output_file)

        # Devolver los resultados
        return resultados_alfabeticos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {e}")
# Nueva ruta para obtener los pilotos en podio
@router.get("/getPodium")
def get_podium():
    output_file_path = os.path.join('app', 'routers', 'podium-predict.json')

    try:
        # Leer el archivo JSON con los resultados
        with open(output_file_path, 'r') as file:
            data = json.load(file)

        # Filtrar los pilotos que estÃ¡n en el podio
        podio = [piloto for piloto in data if piloto.get("Resultado") == "Podio"]

        # Devolver los pilotos en el podio
        return podio

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {e}")
    
@router.get("/fill-Podium")
def fill_podium():
    output_file_path = os.path.join('app', 'routers', 'podium-predict.json')
    try:
        # Leer el archivo JSON con los resultados
        with open(output_file_path, 'r') as file:
            data = json.load(file)
        
        # Crear el diccionario de rutas de imágenes para los pilotos en el podio
        podium_images = []
        for piloto in data:
            if piloto.get("Resultado") == "Podio":
                pilot_name = piloto.get("Piloto")
                if pilot_name in pilot_images:
                    podium_images.append({
                        "Piloto": pilot_name,
                        "shieldImage": pilot_images[pilot_name]["shieldImage"],
                        "pilotImage": pilot_images[pilot_name]["pilotImage"],
                        "carImage": pilot_images[pilot_name]["carImage"]
                    })
        
        # Devolver las rutas de imágenes de los pilotos en el podio
        return podium_images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {e}")