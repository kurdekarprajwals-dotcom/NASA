# ==========================================
# FARMSHIFT AI
# CROP ROTATION ANALYSIS MODULE
# ==========================================


# Crop classification

CROP_FAMILIES = {

    "rice": "cereal",
    "maize": "cereal",
    "wheat": "cereal",
    "sorghum": "cereal",
    "millet": "cereal",

    "chickpea": "legume",
    "kidneybeans": "legume",
    "pigeonpeas": "legume",
    "mothbeans": "legume",
    "mungbean": "legume",
    "blackgram": "legume",
    "lentil": "legume",
    "groundnut": "legume",
    "soybean": "legume",

    "cotton": "fiber",
    "jute": "fiber",

    "mustard": "oilseed",
    "sunflower": "oilseed",
    "sesame": "oilseed",

    "banana": "fruit",
    "mango": "fruit",
    "apple": "fruit",
    "orange": "fruit",
    "grapes": "fruit",
    "papaya": "fruit",
    "coconut": "fruit",
    "pomegranate": "fruit",
    "coffee": "plantation"
}


# ==========================================
# ANALYZE CROP ROTATION
# ==========================================

def analyze_crop_rotation(current_crop, previous_crops):

    current_crop = current_crop.strip().lower()

    previous_crops = [

        crop.strip().lower()

        for crop in previous_crops

        if crop and crop.strip()

    ]

    analysis = []

    # Check repeated crops

    if current_crop in previous_crops:

        analysis.append(
            "The current crop has also been cultivated "
            "in previous seasons. Consider crop rotation "
            "to reduce continuous monocropping risks."
        )

    else:

        analysis.append(
            "The current crop is different from the "
            "recorded previous crops."
        )


    # Identify current crop family

    current_family = CROP_FAMILIES.get(current_crop)


    # Check previous legume cultivation

    previous_legumes = [

        crop for crop in previous_crops

        if CROP_FAMILIES.get(crop) == "legume"

    ]


    if previous_legumes:

        analysis.append(
            "Legume crops were present in the previous "
            "cropping history. Legumes can contribute "
            "to soil nitrogen through biological nitrogen fixation."
        )


    # Check crop family information

    if current_family:

        analysis.append(
            f"The current crop belongs to the "
            f"{current_family} crop family."
        )

    else:

        analysis.append(
            "Crop family information is not available "
            "for the selected crop."
        )


    return {

        "success": True,

        "current_crop": current_crop,

        "previous_crops": previous_crops,

        "current_crop_family": current_family,

        "rotation_analysis": analysis

    }