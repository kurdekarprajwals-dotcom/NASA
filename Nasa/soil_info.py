# FarmShift AI
# Module 5 - Soil Information Collection

import math


def validate_soil_data(soil_data):

    errors = []

    required_fields = [
        "nitrogen",
        "phosphorus",
        "potassium",
        "ph"
    ]

    # Check required fields
    for field in required_fields:

        if field not in soil_data or soil_data[field] == "":
            errors.append(f"{field} is required")

    if errors:
        return False, errors

    try:

        nitrogen = float(soil_data["nitrogen"])
        phosphorus = float(soil_data["phosphorus"])
        potassium = float(soil_data["potassium"])
        ph = float(soil_data["ph"])

    except (ValueError, TypeError):

        return False, ["Please enter valid numerical values"]

    # Reject NaN and infinity
    values = [nitrogen, phosphorus, potassium, ph]

    if not all(math.isfinite(value) for value in values):
        return False, ["Soil values must be finite numbers"]

    # Validate NPK values
    if nitrogen < 0:
        errors.append("Nitrogen cannot be negative")

    if phosphorus < 0:
        errors.append("Phosphorus cannot be negative")

    if potassium < 0:
        errors.append("Potassium cannot be negative")

    # Validate soil pH
    if ph < 0 or ph > 14:
        errors.append("Soil pH must be between 0 and 14")

    if errors:
        return False, errors

    # Organize soil information
    organized_data = {

        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "ph": ph

    }

    return True, organized_data