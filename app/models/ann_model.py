import tensorflow as tf
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Possible values for each categorical column
pilotos = [
    'Max Verstappen', 'Sergio Pérez', 'Carlos Sainz Jr.', 'Charles Leclerc', 'George Russell',
    'Lando Norris', 'Lewis Hamilton', 'Oscar Piastri', 'Fernando Alonso', 'Lance Stroll',
    'Guanyu Zhou', 'Kevin Magnussen', 'Daniel Ricciardo', 'Yuki Tsunoda', 'Alexander Albon',
    'Nico Hülkenberg', 'Esteban Ocon', 'Pierre Gasly', 'Valtteri Bottas', 'Logan Sargeant',
    'Oliver Bearman', 'Franco Colapinto', 'Liam Lawson'
]

circuitos = [
    'bahrain', 'jeddah', 'melbourne', 'suzuka', 'shanghai', 'miami', 'imola', 'monaco', 'montreal',
    'catalunya', 'spielberg', 'silverstone', 'hungaroring', 'spa-francorchamps', 'zandvoort', 'monza',
    'baku', 'marina-bay', 'austin', 'mexico-city', 'interlagos', 'las-vegas', 'losail', 'yas-marina'
]

constructorid = [
    'red-bull', 'ferrari', 'mercedes', 'mclaren', 'aston-martin', 'kick-sauber', 'haas', 'rb', 'williams', 'alpine'
]

# Fit LabelEncoders
label_encoders = {}

# Fit LabelEncoder for Piloto
le_piloto = LabelEncoder()
le_piloto.fit(pilotos)
label_encoders['Piloto'] = le_piloto

# Fit LabelEncoder for Circuito
le_circuito = LabelEncoder()
le_circuito.fit(circuitos)
label_encoders['Circuito'] = le_circuito

# Fit LabelEncoder for ConstructorID
le_constructorid = LabelEncoder()
le_constructorid.fit(constructorid)
label_encoders['ConstructorID'] = le_constructorid

# Save the fitted LabelEncoders
joblib.dump(label_encoders, 'app/label_encoders.pkl')

# Cargar el modelo y los objetos de preprocesamiento
model = tf.keras.models.load_model('model/predict_podium.h5')
scaler = joblib.load("app/scaler.pkl")
label_encoders = joblib.load("app/label_encoders.pkl")

def preprocess_input_data(input_data):
    # Crear DataFrame con los datos de entrada
    data_dict = {
        'Circuito': [input_data.Circuito],
        'ConstructorID': [input_data.ConstructorID],
        'Piloto': [input_data.Piloto],
        'Resultado Clasificacion': [input_data.Resultado_Clasificacion],
        'Promedio Quali': [input_data.Promedio_Quali],
        'Promedio Posición en Circuito': [input_data.Promedio_posicion_circuito],
        'Tasa de Podios': [input_data.Tasa_podios]
    }
    df_input = pd.DataFrame(data_dict)

    # Aplicar el LabelEncoder a las columnas categóricas
    for column in df_input.select_dtypes(include='object').columns:
        # Transformar con los codificadores guardados
        df_input[column] = label_encoders[column].transform(df_input[column])

    # Aplicar el escalador MinMaxScaler
    scaled_data = scaler.transform(df_input)

    return scaled_data

def predict_podium(input_data):
    # Preprocesar los datos de entrada
    processed_data = preprocess_input_data(input_data)
    
    # Hacer la predicción
    prediction = model.predict(processed_data)
    
    # Convertir la predicción a formato binario
    prediction_binary = int(prediction[0][0] > 0.5)
    
    return prediction_binary