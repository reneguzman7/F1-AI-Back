import tensorflow as tf
import numpy as np
import pandas as pd
import joblib

# Cargar el modelo y los objetos de preprocesamiento
model = tf.keras.models.load_model('model/predict_podium.h5')
scaler = joblib.load("app\scaler.pkl")
label_encoders = joblib.load("app\label_encoders.pkl")

def preprocess_input_data(input_data):
    # Crear DataFrame con los datos de entrada
    data_dict = {
        'circuito': [input_data.circuito],
        'constructor_id': [input_data.constructor_id],
        'piloto': [input_data.piloto],
        'resultado_clasificacion': [input_data.resultado_clasificacion],
        'promedio_quali': [input_data.promedio_quali],
        'promedio_posicion_circuito': [input_data.promedio_posicion_circuito],
        'tasa_podios': [input_data.tasa_podios]
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