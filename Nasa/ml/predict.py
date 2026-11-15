# FarmShift AI
# Module 6 - Crop Prediction System

import joblib
import pandas as pd

from pathlib import Path


# Get current file location

BASE_DIR = Path(__file__).resolve().parent


# Load trained ML model

model_path = BASE_DIR / "crop_model.pkl"

model = joblib.load(model_path)


# Collect soil information

print("\n========== FARMER SOIL INFORMATION ==========")

nitrogen = float(input("Enter Nitrogen (N): "))

phosphorus = float(input("Enter Phosphorus (P): "))

potassium = float(input("Enter Potassium (K): "))

ph = float(input("Enter Soil pH: "))


# Collect weather information

print("\n========== WEATHER INFORMATION ==========")

temperature = float(input("Enter Temperature: "))

humidity = float(input("Enter Humidity: "))

rainfall = float(input("Enter Rainfall: "))


# Prepare input data

input_data = pd.DataFrame([{

    "N": nitrogen,

    "P": phosphorus,

    "K": potassium,

    "temperature": temperature,

    "humidity": humidity,

    "ph": ph,

    "rainfall": rainfall

}])


# Predict suitable crop

prediction = model.predict(input_data)


# Display result

print("\n========== CROP RECOMMENDATION ==========")

print("Recommended Crop:", prediction[0])

print("\nCROP PREDICTION COMPLETED!")