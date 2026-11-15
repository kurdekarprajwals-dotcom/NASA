import requests


# NASA POWER API URL
NASA_API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"


def get_nasa_data(latitude, longitude):

    # NASA API parameters
    parameters = {
        "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M",

        "community": "AG",

        "latitude": latitude,

        "longitude": longitude,

        "start": "20251101",

        "end": "20251114",

        "format": "JSON"
    }

    try:

        # Send request to NASA
        response = requests.get(
            NASA_API_URL,
            params=parameters,
            timeout=30
        )

        # Check API response
        response.raise_for_status()

        # Convert JSON response into Python dictionary
        data = response.json()

        # Extract environmental data
        weather_data = data["properties"]["parameter"]

        return weather_data

    except requests.exceptions.RequestException as e:

        print("NASA API Error:", e)

        return None

    except (KeyError, ValueError) as e:

        print("Data extraction error:", e)

        return None