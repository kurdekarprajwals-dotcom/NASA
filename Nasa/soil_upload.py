# FarmShift AI
# Module 5 - Soil Health Card Upload
import pytesseract

from PIL import Image, ImageOps, ImageEnhance

import os

from werkzeug.utils import secure_filename

# Tesseract OCR configuration (uses system-installed tesseract by default)

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# Allowed image formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# Upload folder
UPLOAD_FOLDER = "uploads"


# Maximum file size: 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_soil_image(file):

    # Check whether a file is selected
    if not file or file.filename == "":
        return False, "Please select an image."

    # Check file extension
    filename = secure_filename(file.filename)

    if "." not in filename:
        return False, "Invalid file format."

    extension = filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, "Only JPG, JPEG and PNG images are allowed."

    # Check file size
    file.seek(0, os.SEEK_END)

    file_size = file.tell()

    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return False, "Image size must be less than 5 MB."

    if file_size == 0:
        return False, "Uploaded image is empty."

    return True, filename

# ==========================================
# MODULE 6 - OCR TEXT EXTRACTION
# ==========================================

def extract_text_from_image(image_path):

    try:

        # Open uploaded soil card
        image = Image.open(image_path)

        # Convert image to grayscale
        image = ImageOps.grayscale(image)

        # Improve image contrast
        image = ImageEnhance.Contrast(image).enhance(2)

        # Extract text using Tesseract
        extracted_text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return True, extracted_text

    except Exception as error:

        return False, str(error)

# ==========================================
# MODULE 6 - SOIL PARAMETER EXTRACTION
# ==========================================

import re


def extract_soil_parameters(extracted_text):

    nitrogen = re.search(
        r"Nitrogen[^\d\r\n]{0,30}(\d+(?:\.\d+)?)",
        extracted_text,
        re.IGNORECASE
    )

    phosphorus = re.search(
        r"Phosphorus[^\d\r\n]{0,30}(\d+(?:\.\d+)?)",
        extracted_text,
        re.IGNORECASE
    )

    potassium = re.search(
        r"Potassium[^\d\r\n]{0,30}(\d+(?:\.\d+)?)",
        extracted_text,
        re.IGNORECASE
    )

    ph = re.search(
        r"(?:Soil\s*)?pH[^\d\r\n]{0,15}(\d+(?:\.\d+)?)",
        extracted_text,
        re.IGNORECASE
    )

    soil_data = {

        "nitrogen": float(nitrogen.group(1)) if nitrogen else None,

        "phosphorus": float(phosphorus.group(1)) if phosphorus else None,

        "potassium": float(potassium.group(1)) if potassium else None,

        "ph": float(ph.group(1)) if ph else None

    }

    return soil_data    