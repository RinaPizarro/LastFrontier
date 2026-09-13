
from sql_cities_table import sql_cities_table, alaskan_cities, alaskan_city_coord
from alaskan_cities_text import all_cities_list
from open_weather_api import current_weather_api, lat_and_long, air_pollution_api
from sql_server import create_or_insert
from colorama import Fore, Style, init
from list_functions import output_headers_list, output_values_list, output_to_dict

# REQUIRED TABLES:
# alaskan_cities
# weather
# air_pollution

# This table contains Alaskan cities name, latitude, and longtitude
def cities_table(db_connection):
    cities_list = alaskan_cities()

    for city in cities_list:
        try:
            city_dict = alaskan_city_coord(city)
            create_or_insert(db_connection=db_connection, table_name="alaskan_cities", data_dict=city_dict)
        except AttributeError as a:
            print("Cannot process {city}")
            continue

    print("alaskan_cities table has been created.")

# This table contains weather information of all user selected Alaskan cities from alaskan_cities.txt
def weather_table(db_connection, api_key):
    cities_list = all_cities_list()

    for city in cities_list:

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        print(
            f"\nGetting data for {city}..."
            + Style.RESET_ALL
        )

        # Get city coordinates
        lat, lon = lat_and_long(
            city_name=city
        )

        if lat is None or lon is None:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to find coordinates for {city}."
                + Style.RESET_ALL
            )

            continue

        # Get weather data from API
        status, weather_output = current_weather_api(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if status is False:

            print(
                Fore.LIGHTRED_EX
                + f"Weather API key failed for {city}."
                + Style.RESET_ALL
            )

            return False

        elif status is None:

            print(weather_output)
            return False

        # Convert API output into headers and values
        weather_headers = output_headers_list(
            output=weather_output
        )

        weather_values = output_values_list(
            output=weather_output
        )

        # Convert headers and values into dictionary
        status, weather_data = output_to_dict(
            headers_output=weather_headers,
            values_output=weather_values
        )

        if status is False:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to process weather data for {city}."
                + Style.RESET_ALL
            )

            print(weather_data)
            continue

        # Insert weather data into database
        success, message = create_or_insert(
            db_connection=db_connection,
            table_name="weather",
            data_dict=weather_data
        )

        if success is False:

            print(
                Fore.LIGHTRED_EX
                + f"{city} weather was not inserted."
                + Style.RESET_ALL
            )

            print(message)
            continue

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} weather imported successfully."
            + Style.RESET_ALL
        )

    print(
        Fore.LIGHTGREEN_EX
        + "\nWeather table has been created."
        + Style.RESET_ALL
    )

    return True


# This table contains air pollution information for all user-selected Alaskan cities from alaskan_cities.txt
def air_pollution_table(db_connection, api_key):
    cities_list = all_cities_list()

    for city in cities_list:

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        print(
            f"\nGetting air pollution data for {city}..."
            + Style.RESET_ALL
        )

        # Get city coordinates
        lat, lon = lat_and_long(
            city_name=city
        )

        if lat is None or lon is None:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to find coordinates for {city}."
                + Style.RESET_ALL
            )

            continue

        # Get air pollution data from API
        status, pollution_output = air_pollution_api(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if status is False:

            print(
                Fore.LIGHTRED_EX
                + f"Air pollution API key failed for {city}."
                + Style.RESET_ALL
            )

            return False

        elif status is None:

            print(pollution_output)
            return False

        # Convert API output into headers and values
        pollution_headers = output_headers_list(
            output=pollution_output
        )

        pollution_values = output_values_list(
            output=pollution_output
        )

        # Convert headers and values into dictionary
        status, pollution_data = output_to_dict(
            headers_output=pollution_headers,
            values_output=pollution_values
        )

        if status is False:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to process air pollution data for {city}."
                + Style.RESET_ALL
            )

            print(pollution_data)
            continue

        # Insert air pollution data into database
        success, message = create_or_insert(
            db_connection=db_connection,
            table_name="air_pollution",
            data_dict=pollution_data
        )

        if success is False:

            print(
                Fore.LIGHTRED_EX
                + f"{city} air pollution was not inserted."
                + Style.RESET_ALL
            )

            print(message)
            continue

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} air pollution imported successfully."
            + Style.RESET_ALL
        )

    print(
        Fore.LIGHTGREEN_EX
        + "\nAir pollution table has been created."
        + Style.RESET_ALL
    )

    return Tru
