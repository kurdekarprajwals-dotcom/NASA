# Test Soil Health Card Upload Module

from soil_upload import validate_soil_image

from werkzeug.datastructures import FileStorage

from io import BytesIO


# Create a sample image file
test_image = FileStorage(
    stream=BytesIO(b"Sample soil health card image"),
    filename="soil_card.jpg"
)


# Validate image
status, result = validate_soil_image(test_image)


# Display result
if status:

    print("IMAGE VALIDATION SUCCESSFUL!")
    print("Filename:", result)

else:

    print("IMAGE VALIDATION FAILED!")
    print("Error:", result)