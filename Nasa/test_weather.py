from nasa_api import get_nasa_data

from weather_processing import process_weather_data


# Sample Shivamogga coordinates
latitude = 13.9299
longitude = 75.5681


# Get NASA environmental data
weather_data = get_nasa_data(latitude, longitude)


# Process environmental data
if weather_data:

    processed_data = process_weather_data(weather_data)

    if processed_data:

        print("\nWEATHER PROCESSING SUCCESSFUL!")

        print("\nProcessed Environmental Data:\n")

        for key, value in processed_data.items():

            print(key, ":", value)

    else:

        print("Weather processing failed.")

else:

    print("NASA data retrieval failed.")