# Test Crop Prediction Module

from crop_prediction import predict_crop


# Sample soil information

soil_data = {

    "nitrogen": 90,

    "phosphorus": 42,

    "potassium": 43,

    "ph": 6.5

}


# Sample weather information

weather_data = {

    "average_temperature": 25,

    "average_humidity": 80,

    "total_rainfall": 200

}


# Generate prediction

result = predict_crop(soil_data, weather_data)


# Display result

print("\n========== FARM SHIFT AI ==========")

print(result)