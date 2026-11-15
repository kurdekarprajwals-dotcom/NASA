from nasa_api import get_nasa_data


# Sample Shivamogga coordinates
latitude = 13.9299
longitude = 75.5681


# Get environmental data from NASA
weather = get_nasa_data(latitude, longitude)


# Display results
if weather:

    print("\nNASA POWER DATA RECEIVED SUCCESSFULLY!")

    print("\nTemperature:")
    print(weather["T2M"])

    print("\nHumidity:")
    print(weather["RH2M"])

    print("\nRainfall:")
    print(weather["PRECTOTCORR"])

    print("\nSolar Radiation:")
    print(weather["ALLSKY_SFC_SW_DWN"])

    print("\nWind Speed:")
    print(weather["WS2M"])

else:

    print("Unable to retrieve NASA data.")