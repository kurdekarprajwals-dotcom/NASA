# ==========================================
# IMPORT REQUIRED LIBRARIES
# ==========================================
from ml.crop_prediction import predict_crop
import os
import re
import math
import pytesseract
from crop_rotation import analyze_crop_rotation

from PIL import Image

from flask import Flask, render_template, request, jsonify

from farmer_data import validate_farmer_data
from nasa_api import get_nasa_data
from weather_processing import process_weather_data
from soil_info import validate_soil_data
from soil_upload import (
    validate_soil_image,
    extract_text_from_image,
    extract_soil_parameters
)


# ==========================================
# TESSERACT CONFIGURATION
# ==========================================

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# ==========================================
# INITIALIZE FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# SOIL HEALTH CARD UPLOAD CONFIGURATION
# ==========================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# RECEIVE FARMER INFORMATION
# ==========================================

@app.route("/api/farmer-data", methods=["POST"])
def submit_farmer_data():

    try:

        # Receive JSON data
        data = request.get_json()

        if not isinstance(data, dict):

            return jsonify({
                "success": False,
                "message": "Invalid request data."
            }), 400

        # Validate farmer information
        farmer, errors = validate_farmer_data(data)

        if errors:

            return jsonify({
                "success": False,
                "errors": errors
            }), 400

        # Extract GPS coordinates
        latitude = farmer["location"]["latitude"]

        longitude = farmer["location"]["longitude"]

        # Retrieve NASA environmental data
        weather_data = get_nasa_data(latitude, longitude)

        if not weather_data:

            return jsonify({
                "success": False,
                "message": "Unable to retrieve NASA environmental data."
            }), 502

        # Process weather information
        processed_weather = process_weather_data(weather_data)

        if not processed_weather:

            return jsonify({
                "success": False,
                "message": "Unable to process environmental data."
            }), 500

        # Successful response
        return jsonify({

            "success": True,

            "message": "Farmer information and environmental data collected successfully!",

            "farmer_data": farmer,

            "weather_data": processed_weather

        }), 200

    except Exception as e:

        print("Farmer Data Error:", e)

        return jsonify({
            "success": False,
            "message": "Something went wrong."
        }), 500


# ==========================================
# SOIL INFORMATION VALIDATION
# ==========================================

@app.route("/api/soil-data", methods=["POST"])
def submit_soil_data():

    try:

        # Receive soil information
        data = request.get_json()

        if not isinstance(data, dict):

            return jsonify({
                "success": False,
                "message": "Invalid soil information."
            }), 400

        # Extract soil information
        soil_data = data.get("soil_data")

        if not isinstance(soil_data, dict):

            return jsonify({
                "success": False,
                "errors": ["Soil information is required."]
            }), 400

        # Validate soil information
        soil_status, soil_result = validate_soil_data(soil_data)

        if not soil_status:

            return jsonify({
                "success": False,
                "errors": soil_result
            }), 400

        # Successful response
        return jsonify({

            "success": True,

            "message": "Soil information collected successfully!",

            "soil_data": soil_result

        }), 200

    except Exception as e:

        print("Soil Error:", e)

        return jsonify({
            "success": False,
            "message": "Something went wrong while processing soil information."
        }), 500


# ==========================================
# SOIL HEALTH CARD UPLOAD AND OCR
# ==========================================

@app.route("/api/soil-upload", methods=["POST"])
def upload_soil_card():

    try:

        # Check uploaded file
        if "soil_image" not in request.files:

            return jsonify({
                "success": False,
                "message": "No image uploaded."
            }), 400

        file = request.files["soil_image"]

        # Validate image
        status, result = validate_soil_image(file)

        if not status:

            return jsonify({
                "success": False,
                "message": result
            }), 400

        # Save image
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            result
        )

        file.save(file_path)

        # Open image
        image = Image.open(file_path)

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)

        # Extract nitrogen
        nitrogen = re.search(
            r"Nitrogen\s*\(?N\)?\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            extracted_text,
            re.IGNORECASE
        )

        # Extract phosphorus
        phosphorus = re.search(
            r"Phosphorus\s*\(?P\)?\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            extracted_text,
            re.IGNORECASE
        )

        # Extract potassium
        potassium = re.search(
            r"Potassium\s*\(?K\)?\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            extracted_text,
            re.IGNORECASE
        )

        # Extract pH
        ph = re.search(
            r"Soil\s*pH\s*[:\-]?\s*(\d+(?:\.\d+)?)",
            extracted_text,
            re.IGNORECASE
        )

        # Store extracted values
        soil_data = {

            "nitrogen": float(nitrogen.group(1)) if nitrogen else None,

            "phosphorus": float(phosphorus.group(1)) if phosphorus else None,

            "potassium": float(potassium.group(1)) if potassium else None,

            "ph": float(ph.group(1)) if ph else None

        }

        # Check extracted parameters
        if None in soil_data.values():

            return jsonify({

                "success": False,

                "message": "Unable to extract all soil parameters. Please upload a clearer Soil Health Card.",

                "soil_data": soil_data

            }), 422

        # Validate extracted soil values
        soil_status, soil_result = validate_soil_data(soil_data)

        if not soil_status:

            return jsonify({

                "success": False,

                "message": "Extracted soil information is invalid.",

                "errors": soil_result

            }), 422

        # Successful response
        return jsonify({

            "success": True,

            "message": "Soil Health Card processed successfully!",

            "filename": result,

            "soil_data": soil_result

        }), 200

    except Exception as e:

        print("OCR Upload Error:", e)

        return jsonify({

            "success": False,

            "message": "Unable to process Soil Health Card."

        }), 500

# Crop Recommendation API

@app.route("/api/recommend-crop", methods=["POST"])
def recommend_crop():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request data is required."
        }), 400

    # Get soil and weather information
    soil_data = data.get("soil_data")
    weather_data = data.get("weather_data")

    if not isinstance(soil_data, dict):
        return jsonify({
            "success": False,
            "message": "Soil information is required."
        }), 400

    if not isinstance(weather_data, dict):
        return jsonify({
            "success": False,
            "message": "Weather information is required."
        }), 400

    # Validate soil information
    soil_status, soil_result = validate_soil_data(soil_data)

    if not soil_status:
        return jsonify({
            "success": False,
            "errors": soil_result
        }), 400

    # Generate crop prediction
    result = predict_crop(soil_result, weather_data)

    if not result["success"]:
        return jsonify({
            "success": False,
            "message": result["message"]
        }), 500

    return jsonify({
        "success": True,
        "message": "Crop recommendation generated successfully!",
        "recommended_crop": result["recommended_crop"]
    }), 200

# ==========================================
# CROP ROTATION ANALYSIS API
# ==========================================

@app.route("/api/crop-rotation", methods=["POST"])
def crop_rotation():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message": "Request data is required."

        }), 400


    # Get crop information

    current_crop = data.get("current_crop")

    previous_crops = data.get("previous_crops", [])


    # Validate current crop

    if not isinstance(current_crop, str) or not current_crop.strip():

        return jsonify({

            "success": False,

            "message": "Current crop information is required."

        }), 400


    # Validate previous crops

    if not isinstance(previous_crops, list):

        return jsonify({

            "success": False,

            "message": "Previous crops must be provided as a list."

        }), 400


    # Generate crop rotation analysis

    result = analyze_crop_rotation(
        current_crop,
        previous_crops
    )


    return jsonify({

        "success": True,

        "message": "Crop rotation analysis completed successfully!",

        "rotation_result": result

    }), 200
# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)