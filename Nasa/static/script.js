
// =====================================
// 1. STORE FARMER GPS COORDINATES
// =====================================

let farmerLocation = null;


// =====================================
// 2. DETECT FARMER LOCATION
// =====================================

document.getElementById("locationBtn")
.addEventListener("click", function () {

    const status = document.getElementById("locationStatus");

    if (!navigator.geolocation) {

        status.innerText = "GPS is not supported by your browser.";
        return;

    }

    status.innerText = "Detecting location...";

    navigator.geolocation.getCurrentPosition(

        function (position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            farmerLocation = {
                latitude: latitude,
                longitude: longitude
            };

            document.getElementById("latitude").innerText =
                latitude.toFixed(5);

            document.getElementById("longitude").innerText =
                longitude.toFixed(5);

            status.innerText = "Location detected successfully!";

        },

        function (error) {

            console.error("GPS Error:", error);

            status.innerText =
                "Unable to access location. Please allow GPS permission.";

        },

        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }

    );

});


// =====================================
// 3. SUBMIT FARMER INFORMATION
// =====================================

document.getElementById("farmerForm")
.addEventListener("submit", async function (event) {

    event.preventDefault();

    const message = document.getElementById("message");
    const result = document.getElementById("result");
    const submitBtn = document.getElementById("submitBtn");

    const recommendationSection =
        document.getElementById("recommendationSection");

    const recommendationStatus =
        document.getElementById("recommendationStatus");

    const recommendedCrop =
        document.getElementById("recommendedCrop");


    // =====================================
    // CHECK GPS LOCATION
    // =====================================

    if (!farmerLocation) {

        message.innerText =
            "Please detect your farm location first.";

        message.style.color = "red";
        return;

    }


    // =====================================
    // COLLECT PREVIOUS CROPS
    // =====================================

    const previousCrops = [

        document.getElementById("previousCrop1").value.trim(),

        document.getElementById("previousCrop2").value.trim(),

        document.getElementById("previousCrop3").value.trim()

    ].filter(crop => crop !== "");


    // =====================================
    // COLLECT FARMER PRIORITIES
    // =====================================

    const priorities = Array.from(

        document.querySelectorAll(
            'input[name="priority"]:checked'
        )

    ).map(item => item.value);


    if (priorities.length === 0) {

        message.innerText =
            "Please select at least one priority.";

        message.style.color = "red";
        return;

    }


    // =====================================
    // COLLECT SOIL INFORMATION
    // =====================================

    const selectedSoilMethod = document.querySelector(
        'input[name="soilMethod"]:checked'
    ).value;

    let soilData = {};


    if (selectedSoilMethod === "manual") {

        soilData = {

            nitrogen: document.getElementById("nitrogen").value,

            phosphorus: document.getElementById("phosphorus").value,

            potassium: document.getElementById("potassium").value,

            ph: document.getElementById("soilPH").value

        };

    }

    else {

        soilData = {

            nitrogen: document.getElementById("extractedNitrogen").value,

            phosphorus: document.getElementById("extractedPhosphorus").value,

            potassium: document.getElementById("extractedPotassium").value,

            ph: document.getElementById("extractedPH").value

        };

    }


    // =====================================
    // COLLECT FARMER INFORMATION
    // =====================================

    const farmerData = {

        latitude: farmerLocation.latitude,

        longitude: farmerLocation.longitude,

        land_area: document.getElementById("landArea").value,

        soil_type: document.getElementById("soilType").value,

        soil_data: soilData,

        current_crop:
            document.getElementById("currentCrop").value.trim(),

        previous_crops: previousCrops,

        water_availability:
            document.getElementById("waterAvailability").value,

        season: document.getElementById("season").value,

        priorities: priorities

    };


    // =====================================
    // START SUBMISSION
    // =====================================

    submitBtn.disabled = true;
    submitBtn.innerText = "Processing...";

    message.innerText = "";
    result.innerText = "";

    recommendationSection.style.display = "none";

    recommendedCrop.innerText = "--";


    // Reset rotation dashboard

    document.getElementById("rotationStatus").innerText =
        "Waiting for crop rotation analysis...";

    document.getElementById("rotationCurrentCrop").innerText = "--";

    document.getElementById("rotationPreviousCrops").innerText = "--";

    document.getElementById("rotationInsights").innerHTML = "";


    try {


        // =====================================
        // STEP 1: VALIDATE SOIL INFORMATION
        // =====================================

        message.innerText =
            "Validating soil information...";

        message.style.color = "blue";


        const soilResponse = await fetch("/api/soil-data", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                soil_data: soilData

            })

        });


        const soilResult = await soilResponse.json();


        if (!soilResponse.ok) {

            const errors = soilResult.errors || [
                soilResult.message
            ];

            throw new Error(errors.filter(Boolean).join("\n"));

        }


        // =====================================
        // STEP 2: SUBMIT FARMER INFORMATION
        // =====================================

        message.innerText =
            "Processing farmer information and NASA weather data...";


        const response = await fetch("/api/farmer-data", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(farmerData)

        });


        const data = await response.json();


        if (!response.ok) {

            const errors = data.errors || [
                data.message
            ];

            throw new Error(errors.filter(Boolean).join("\n"));

        }


        // =====================================
        // STEP 3: CHECK WEATHER INFORMATION
        // =====================================

        if (!data.weather_data) {

            throw new Error(
                "Weather information was not received from the server."
            );

        }


        // =====================================
        // STEP 4: GENERATE ML CROP PREDICTION
        // =====================================

        message.innerText =
            "Generating crop recommendation using AI and ML...";

        recommendationSection.style.display = "block";

        recommendationStatus.innerText =
            "Analyzing soil and weather conditions...";


        const cropResponse = await fetch("/api/recommend-crop", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                soil_data: soilResult.soil_data,

                weather_data: data.weather_data

            })

        });


        const cropResult = await cropResponse.json();


        if (!cropResponse.ok) {

            throw new Error(
                cropResult.message ||
                "Crop recommendation failed."
            );

        }


        // =====================================
        // STEP 5: DISPLAY CROP RECOMMENDATION
        // =====================================

        if (!cropResult.recommended_crop) {

            throw new Error(
                "ML model did not return a recommended crop."
            );

        }


        recommendedCrop.innerText =
            cropResult.recommended_crop;


        // =====================================
        // DISPLAY DASHBOARD INFORMATION
        // =====================================

        // SOIL DETAILS

        document.getElementById("dashNitrogen").innerText =
            soilResult.soil_data.nitrogen;

        document.getElementById("dashPhosphorus").innerText =
            soilResult.soil_data.phosphorus;

        document.getElementById("dashPotassium").innerText =
            soilResult.soil_data.potassium;

        document.getElementById("dashPH").innerText =
            soilResult.soil_data.ph;


        // WEATHER DETAILS

        document.getElementById("dashTemperature").innerText =
            data.weather_data.average_temperature + " °C";

        document.getElementById("dashHumidity").innerText =
            data.weather_data.average_humidity + " %";

        document.getElementById("dashRainfall").innerText =
            data.weather_data.total_rainfall + " mm";


        // FARMING INFORMATION

        document.getElementById("dashLandArea").innerText =
            farmerData.land_area;

        document.getElementById("dashSoilType").innerText =
            farmerData.soil_type;

        document.getElementById("dashWater").innerText =
            farmerData.water_availability;

        document.getElementById("dashSeason").innerText =
            farmerData.season;


        // AI EXPLANATION

        document.getElementById("aiExplanation").innerText =

            "The Random Forest Machine Learning model analyzed " +
            "your soil nutrient values, soil pH, temperature, " +
            "humidity and rainfall to predict a suitable crop: " +
            cropResult.recommended_crop + ".";


        recommendationStatus.innerText =
            cropResult.message ||
            "Crop recommendation generated successfully!";


        // =====================================
        // STEP 6: CROP ROTATION ANALYSIS
        // =====================================

        message.innerText =
            "Analyzing previous cropping history...";


        try {

            const rotationResponse = await fetch("/api/crop-rotation", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    current_crop: farmerData.current_crop,

                    previous_crops: farmerData.previous_crops

                })

            });


            const rotationData = await rotationResponse.json();


            if (!rotationResponse.ok) {

                throw new Error(
                    rotationData.message ||
                    "Crop rotation analysis failed."
                );

            }


            // =====================================
            // DISPLAY ROTATION ANALYSIS
            // =====================================

            const rotationResult = rotationData.rotation_result;


            document.getElementById("rotationCurrentCrop").innerText =
                rotationResult.current_crop;


            document.getElementById("rotationPreviousCrops").innerText =

                rotationResult.previous_crops.length > 0

                    ? rotationResult.previous_crops.join(", ")

                    : "No previous crop information provided.";


            const rotationInsights = document.getElementById(
                "rotationInsights"
            );

            rotationInsights.innerHTML = "";


            rotationResult.rotation_analysis.forEach(function (insight) {

                const li = document.createElement("li");

                li.textContent = insight;

                rotationInsights.appendChild(li);

            });


            document.getElementById("rotationStatus").innerText =
                "Crop rotation analysis completed successfully!";


            console.log("Crop Rotation Result:", rotationResult);


        }

        catch (rotationError) {

            console.error("Crop Rotation Error:", rotationError);

            document.getElementById("rotationStatus").innerText =
                "Crop rotation analysis could not be completed.";

        }


        // =====================================
        // STEP 7: DISPLAY COMPLETE RESULTS
        // =====================================

        message.innerText =
            "FarmShift AI analysis completed successfully!";

        message.style.color = "green";


        result.innerText = JSON.stringify({

            farmer_data: data.farmer_data,

            soil_data: soilResult.soil_data,

            weather_data: data.weather_data,

            recommended_crop: cropResult.recommended_crop

        }, null, 4);


        // =====================================
        // CONSOLE OUTPUTS
        // =====================================

        console.log("Farmer Data:", data.farmer_data);

        console.log("Soil Data:", soilResult.soil_data);

        console.log("Weather Data:", data.weather_data);

        console.log(
            "Recommended Crop:",
            cropResult.recommended_crop
        );


        // =====================================
        // SCROLL TO RECOMMENDATION
        // =====================================

        recommendationSection.scrollIntoView({

            behavior: "smooth",

            block: "center"

        });


    }


    catch (error) {

        message.innerText = error.message;

        message.style.color = "red";

        console.error("FarmShift AI Error:", error);

        recommendationStatus.innerText =
            "Unable to generate crop recommendation.";

    }


    finally {

        submitBtn.disabled = false;

        submitBtn.innerText =
            "Submit Farmer Information";

    }

});


// =====================================
// 4. SOIL INFORMATION MODULE
// =====================================

const soilMethodOptions = document.querySelectorAll(
    'input[name="soilMethod"]'
);


const manualSoilSection = document.getElementById(
    "manualSoilSection"
);


const soilUploadSection = document.getElementById(
    "soilUploadSection"
);


soilMethodOptions.forEach(option => {

    option.addEventListener("change", function () {

        if (this.value === "manual") {

            manualSoilSection.style.display = "block";

            soilUploadSection.style.display = "none";

        }

        else {

            manualSoilSection.style.display = "none";

            soilUploadSection.style.display = "block";

        }

    });

});


// =====================================
// 5. SOIL HEALTH CARD IMAGE PREVIEW
// =====================================

const soilCardImage = document.getElementById("soilCardImage");

const soilImagePreview = document.getElementById("soilImagePreview");

const previewImage = document.getElementById("previewImage");


soilCardImage.addEventListener("change", function () {

    const file = this.files[0];


    if (!file) {

        soilImagePreview.style.display = "none";

        return;

    }


    if (!file.type.startsWith("image/")) {

        alert("Please upload a valid image.");

        this.value = "";

        soilImagePreview.style.display = "none";

        return;

    }


    if (file.size > 5 * 1024 * 1024) {

        alert("Image size must be less than 5 MB.");

        this.value = "";

        soilImagePreview.style.display = "none";

        return;

    }


    const imageURL = URL.createObjectURL(file);

    previewImage.src = imageURL;

    soilImagePreview.style.display = "block";

});


// =====================================
// 6. SOIL HEALTH CARD OCR INTEGRATION
// =====================================

const extractSoilBtn = document.getElementById("extractSoilBtn");

const ocrStatus = document.getElementById("ocrStatus");


extractSoilBtn.addEventListener("click", async function () {

    const file = soilCardImage.files[0];


    if (!file) {

        ocrStatus.innerText =
            "Please upload a Soil Health Card first.";

        ocrStatus.style.color = "red";

        return;

    }


    const formData = new FormData();

    formData.append("soil_image", file);


    extractSoilBtn.disabled = true;

    extractSoilBtn.innerText = "Extracting...";

    ocrStatus.innerText =
        "Processing Soil Health Card...";

    ocrStatus.style.color = "blue";


    try {

        const response = await fetch("/api/soil-upload", {

            method: "POST",

            body: formData

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(

                data.message ||

                (data.errors && data.errors.join("\n")) ||

                "OCR extraction failed."

            );

        }


        // =====================================
        // DISPLAY EXTRACTED SOIL INFORMATION
        // =====================================

        if (data.soil_data) {

            document.getElementById("extractedNitrogen").value =
                data.soil_data.nitrogen ?? "";

            document.getElementById("extractedPhosphorus").value =
                data.soil_data.phosphorus ?? "";

            document.getElementById("extractedPotassium").value =
                data.soil_data.potassium ?? "";

            document.getElementById("extractedPH").value =
                data.soil_data.ph ?? "";

        }


        ocrStatus.innerText = data.message;

        ocrStatus.style.color = "green";


    }


    catch (error) {

        ocrStatus.innerText = error.message;

        ocrStatus.style.color = "red";

        console.error("OCR Error:", error);

    }


    finally {

        extractSoilBtn.disabled = false;

        extractSoilBtn.innerText =
            "Extract Soil Details";

    }

});
