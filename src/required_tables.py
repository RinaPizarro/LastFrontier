from cities_table import alaskan_cities, alaskan_city_coord
from user_cities import all_cities_list
from open_weather_api import current_weather_api, lat_and_long, air_pollution_api
from sql_server import create_or_insert, find_existing_row
from column_functions import output_headers_list, output_values_list, output_to_dict
from colorama import Fore, Style, init

# REQUIRED TABLES:
# alaskan_cities
# weather
# air_pollution

# This table contains Alaskan cities name, latitude, and longtitude
def cities_table(db_connection, cities_list):
    table_message_shown = False
    table_name = "alaskan_cities"

    for city in cities_list:

        print(f"\nGetting data for {city}...")

        # Get city coordinates
        city_output = alaskan_city_coord(city)

        if city_output is None:
            print(f"Unable to find coordinates for {city}.")
            continue

        # Convert API output
        city_headers = output_headers_list(
            output=city_output
        )

        city_values = output_values_list(
            output=city_output
        )

        success, city_data = output_to_dict(
            headers_output=city_headers,
            values_output=city_values
        )

        if success is False:
            print(f"Unable to process city data for {city}.")
            print(city_data)
            continue

        # Insert city data (if lat and lon have not changed)
        if find_existing_row(db_connection=db_connection,table_name=table_name,rows_dict=city_data) > 0:
            print(f'Latitude and Longtitude for {city} has not changed. Skipping...')
        else:
            success, message = create_or_insert(
                db_connection=db_connection,
                table_name=table_name,
                data_dict=city_data
            )

            if success is False:
                print(f"{city} was not inserted.")
                print(message)
                continue

            # Print table status only once
            if table_message_shown is False:

                print(message)

                table_message_shown = True

            print(f"{city} imported successfully.")

    print("alaskan_cities table has been processed.")

    return True


# This table contains weather information of all user selected Alaskan cities from alaskan_cities.txt
def weather_table(db_connection, api_key, cities_list):

    table_message_shown = False

    for city in cities_list:

        print(f"\nGetting data for {city}...")

        # Get city coordinates
        lat, lon = lat_and_long(
            city_name=city
        )

        if lat is None or lon is None:
            print(
                + f"Unable to find coordinates for {city}."
                + Style.RESET_ALL
            )
            continue

        # Get weather data
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

        # Convert API output
        weather_headers = output_headers_list(
            output=weather_output
        )

        weather_values = output_values_list(
            output=weather_output
        )

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

        # Insert weather data
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

        # Print table status only once
        if table_message_shown is False:

            print(
                Fore.LIGHTYELLOW_EX
                + message
                + Style.RESET_ALL
            )

            table_message_shown = True

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} weather imported successfully."
            + Style.RESET_ALL
        )

    return True

# This table contains air pollution information for all user-selected Alaskan cities from alaskan_cities.txt
def air_pollution_table(db_connection, api_key, cities_list):
    table_message_shown = False

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

        # Get air pollution data
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

        # Convert API output
        pollution_headers = output_headers_list(
            output=pollution_output
        )

        pollution_values = output_values_list(
            output=pollution_output
        )

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

        # Insert air pollution data
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

        # Print table status only once
        if table_message_shown is False:

            print(
                Fore.LIGHTYELLOW_EX
                + message
                + Style.RESET_ALL
            )

            table_message_shown = True

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} air pollution imported successfully."
            + Style.RESET_ALL
        )

    return True