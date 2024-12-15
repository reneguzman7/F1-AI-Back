import requests
import json
import os
# Ruta al archivo JSON
file_path = os.path.join('app', 'routers', 'data.json')
# URL de la API
url = "https://f1-ai-back.onrender.com/predict"

# Inicializar contadores
podio_count = 0
fuera_podio_count = 0

# Leer el archivo JSON
with open(file_path, 'r') as file:
    data = json.load(file)

# Procesar cada piloto
for piloto in data:
    try:
        # Enviar POST
        response = requests.post(url, json=piloto)

        # Verificar respuesta
        if response.status_code == 200:
            result = response.json().get("podio", None)
            if result == 1:
                podio_count += 1
            elif result == 0:
                fuera_podio_count += 1
            else:
                print(f"Respuesta inesperada para piloto: {piloto}")
        else:
            print(f"Error en la solicitud para {piloto}: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error procesando piloto {piloto}: {e}")

# Resultados finales
print(f"Pilotos en podio: {podio_count}")
print(f"Pilotos fuera de podio: {fuera_podio_count}")
