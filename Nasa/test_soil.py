# Testing FarmShift AI Soil Module

from soil_info import validate_soil_data


# Sample soil testing report data
soil_data = {
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "ph": 6.5
}


# Validate soil information
status, result = validate_soil_data(soil_data)


# Display result
if status:

    print("SOIL VALIDATION SUCCESSFUL!")
    print("Validated Soil Information:")
    print(result)

else:

    print("SOIL VALIDATION FAILED!")
    print("Errors:")
    print(result)