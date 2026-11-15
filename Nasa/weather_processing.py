# FarmShift AI
# Weather Processing Module


def process_weather_data(weather_data):

    try:

        temperatures = weather_data["T2M"]

        humidity = weather_data["RH2M"]

        rainfall = weather_data["PRECTOTCORR"]

        # Drop missing values (NASA uses -99 as sentinel)

        temps = [v for v in temperatures.values() if v > -90]

        hums = [v for v in humidity.values() if v > -90]

        rains = [v for v in rainfall.values() if v >= 0]

        if not temps or not hums or not rains:

            return None

        processed = {

            "average_temperature": round(sum(temps) / len(temps), 2),

            "average_humidity": round(sum(hums) / len(hums), 2),

            "total_rainfall": round(sum(rains), 2)

        }

        return processed

    except (KeyError, TypeError, ValueError) as e:

        print("Weather Processing Error:", e)

        return None
