# Farmer data validation module


# Allowed soil types
SOIL_TYPES = [
    "Sandy",
    "Clay",
    "Silty",
    "Loamy",
    "Clay Loam",
    "Sandy Loam",
    "Don't know"
]


# Allowed water availability options
WATER_OPTIONS = [
    "Rainfed",
    "Limited Irrigation",
    "Moderate Irrigation",
    "Good Irrigation"
]


# Allowed farming seasons
SEASONS = [
    "Kharif",
    "Rabi",
    "Zaid",
    "Year-round",
    "Not sure"
]


# Allowed farmer priorities
PRIORITIES = [
    "Improve Soil Health",
    "Save Water",
    "Increase Crop Yield",
    "Reduce Farming Risks",
    "Adapt to Climate Change"
]


def validate_farmer_data(data):

    errors = []

    # 1. Get location information
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    try:
        latitude = float(latitude)
        longitude = float(longitude)

        if not -90 <= latitude <= 90:
            errors.append("Invalid latitude.")

        if not -180 <= longitude <= 180:
            errors.append("Invalid longitude.")

    except (TypeError, ValueError):
        errors.append("Valid GPS coordinates are required.")

    # 2. Get land area
    try:
        land_area = float(data.get("land_area"))

        if land_area <= 0:
            errors.append("Land area must be greater than zero.")

    except (TypeError, ValueError):
        land_area = None
        errors.append("Enter a valid land area.")

    # 3. Get soil type
    soil_type = data.get("soil_type")

    if soil_type not in SOIL_TYPES:
        errors.append("Please select a valid soil type.")

    # 4. Get current crop
    current_crop = data.get("current_crop")

    if not isinstance(current_crop, str) or not current_crop.strip():
        errors.append("Current crop is required.")
    elif len(current_crop.strip()) > 50:
        errors.append("Current crop name is too long.")
    else:
        current_crop = current_crop.strip()

    # 5. Get previous crops
    previous_crops = data.get("previous_crops")

    if not isinstance(previous_crops, list):
        errors.append("Previous crops must be provided as a list.")
        previous_crops = []

    elif len(previous_crops) > 3:
        errors.append("Enter a maximum of three previous crops.")

    else:
        cleaned_crops = []

        for crop in previous_crops:

            if not isinstance(crop, str) or not crop.strip():
                errors.append("Invalid previous crop name.")
                break

            if len(crop.strip()) > 50:
                errors.append("Previous crop name is too long.")
                break

            cleaned_crops.append(crop.strip())

        previous_crops = cleaned_crops

    # 6. Get water availability
    water_availability = data.get("water_availability")

    if water_availability not in WATER_OPTIONS:
        errors.append("Please select water availability.")

    # 7. Get farming season
    season = data.get("season")

    if season not in SEASONS:
        errors.append("Please select a valid farming season.")

    # 8. Get farmer priorities
    priorities = data.get("priorities")

    if not isinstance(priorities, list) or len(priorities) == 0:
        errors.append("Select at least one farming priority.")

        priorities = []

    else:

        for priority in priorities:

            if priority not in PRIORITIES:
                errors.append("Invalid farming priority.")
                break

        if len(set(priorities)) != len(priorities):
            errors.append("Duplicate farming priorities are not allowed.")

    # Stop if validation fails
    if errors:
        return None, errors

    # Organize farmer information
    farmer_data = {

        "location": {
            "latitude": latitude,
            "longitude": longitude
        },

        "land_area": land_area,

        "soil_type": soil_type,

        "current_crop": current_crop,

        "previous_crops": previous_crops,

        "water_availability": water_availability,

        "season": season,

        "priorities": priorities

    }

    return farmer_data, []