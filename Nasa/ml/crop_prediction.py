# FarmShift AI
# Crop Prediction Module

import joblib
import pandas as pd

from pathlib import Path


# Load trained model

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "crop_model.pkl"

model = joblib.load(MODEL_PATH)


# Crop prediction function

def predict_crop(soil_data, weather_data):

    try:

        # Prepare ML input

        input_data = pd.DataFrame([{

            "N": float(soil_data["nitrogen"]),

            "P": float(soil_data["phosphorus"]),

            "K": float(soil_data["potassium"]),

            "temperature": float(weather_data["average_temperature"]),

            "humidity": float(weather_data["average_humidity"]),

            "ph": float(soil_data["ph"]),

            "rainfall": float(weather_data["total_rainfall"])

        }])

        # Predict crop

        prediction = model.predict(input_data)

        return {

            "success": True,

            "recommended_crop": prediction[0]

        }

    except Exception as e:

        print("Crop Prediction Error:", e)

        return {

            "success": False,

            "message": "Unable to generate crop recommendation."

        }