import pytesseract
from PIL import Image
import re


# Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Load Soil Health Card image
image = Image.open("uploads/sample_soil_card.png")


# Extract text using OCR
extracted_text = pytesseract.image_to_string(image)


print("\nExtracted Text:")
print("--------------------")
print(extracted_text)


# --------------------------------
# EXTRACT SOIL PARAMETERS
# --------------------------------

# Nitrogen
nitrogen = re.search(
    r"Nitrogen\s*\(?N\)?\s*(\d+(?:\.\d+)?)",
    extracted_text,
    re.IGNORECASE
)


# Phosphorus
phosphorus = re.search(
    r"Phosphorus\s*\(?P\)?\s*(\d+(?:\.\d+)?)",
    extracted_text,
    re.IGNORECASE
)


# Potassium
potassium = re.search(
    r"Potassium\s*\(?K\)?\s*(\d+(?:\.\d+)?)",
    extracted_text,
    re.IGNORECASE
)


# Soil pH
ph = re.search(
    r"Soil\s*pH\s*(\d+(?:\.\d+)?)",
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


print("\nExtracted Soil Parameters:")
print(soil_data)