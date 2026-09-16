from lastfrontier.cities_table import (
    all_alaskan_cities,
    alaskan_city_coord
)

from lastfrontier.custom_cities import (
    clean_cities
)

from lastfrontier.open_weather_api import (
    current_weather_api,
    lat_and_long,
    air_pollution_api
)

from lastfrontier.sql_server import (
    connection,
    create_table,
    insert_data,
    find_existing_row,
    find_table
)

from lastfrontier.column_functions import (
    output_headers_list,
    output_values_list,
    output_to_dict
)

from colorama import Fore, Style
from pathlib import Path

import os
import json

TABLES_FILE = (Path(__file__).resolve().parent / "data" / "tables.json")


API_FUNCTIONS = {
    "current_weather_api": current_weather_api,
    "air_pollution_api": air_pollution_api
}

def load_table_config():
    with open(TABLES_FILE, "r") as file:
        return json.load(file)


def get_table_config(table_name):
    TABLE_CONFIG = load_table_config()

    if table_name not in TABLE_CONFIG:
        raise ValueError(
            f"Unknown table: {table_name}"
        )

    return TABLE_CONFIG[table_name]

def get_api_function(table_name):
    config = get_table_config(table_name)

    api_name = config.get("api_func")

    if not api_name:
        return False, None

    api_function = API_FUNCTIONS.get(api_name)

    if api_function is None:
        return False, (
            f"API function '{api_name}' is not registered."
        )

    return True, api_function

def required_table_create(table_name):
    db_status, db_connection = connection()

    if not db_status:
        return False, db_connection

    config = get_table_config(table_name)

    table_type = config.get("type")

    if table_type == "Master":

        cities_list = all_alaskan_cities(count=1)

        if not cities_list:
            return False, (
                "No Alaskan cities were found."
            )

        city = cities_list[0]

        city_output = alaskan_city_coord(
            city_name=city
        )

        if city_output is None:
            return False, (
                f"Unable to find coordinates for {city}."
            )

        headers_list = output_headers_list(
            output=city_output
        )

        values_list = output_values_list(
            output=city_output
        )

    elif config.get("api_func"):

        api_key = os.getenv(
            "OPEN_WEATHER_API_KEY"
        )

        if not api_key:
            return False, (
                "OPEN_WEATHER_API_KEY is not set."
            )

        cities_list = clean_cities()

        if not cities_list:
            return False, (
                "No cities were found."
            )

        city = cities_list[0]

        lat, lon = lat_and_long(
            city_name=city
        )

        if lat is None or lon is None:
            return False, (
                f"Unable to find coordinates for {city}."
            )

        success, api_function = get_api_function(
            table_name
        )

        if not success:
            return False, api_function

        status, api_output = api_function(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if not status:
            return False, api_output

        headers_list = output_headers_list(
            output=api_output
        )

        values_list = output_values_list(
            output=api_output
        )

    else:

        return False, (
            f"Unsupported table configuration "
            f"for table '{table_name}'."
        )

    status, message = create_table(
        db_connection=db_connection,
        table_name=table_name,
        column_names=headers_list,
        column_values=values_list
    )

    return status, message


def insert_master_table(
    table_name,
    db_connection
):

    cities_list = all_alaskan_cities()

    for city in cities_list:

        print(
            f"\nGetting data for {city}..."
        )

        city_output = alaskan_city_coord(
            city_name=city
        )

        if city_output is None:

            print(
                f"Unable to find coordinates for {city}."
            )

            continue

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

        if not success:

            print(
                f"Unable to process city data "
                f"for {city}."
            )

            print(city_data)

            continue

        status, count = find_existing_row(
            db_connection=db_connection,
            table_name=table_name,
            rows_dict=city_data
        )

        if not status:

            print(
                f"Unable to check existing data "
                f"for {city}."
            )

            print(count)

            continue

        if int(count) > 0:

            print(
                f"Latitude and Longitude for {city} "
                "has not changed. Skipping..."
            )

            continue

        success, message = insert_data(
            db_connection=db_connection,
            table_name=table_name,
            data_dict=city_data
        )

        if not success:

            print(
                f"{city} was not inserted."
            )

            print(message)

            continue

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} imported successfully."
            + Style.RESET_ALL
        )

    print(
        f"\n{table_name} table has been processed."
    )

    return True


def insert_api_table(
    table_name,
    db_connection
):

    api_key = os.getenv(
        "OPEN_WEATHER_API_KEY"
    )

    if not api_key:

        print(
            Fore.LIGHTRED_EX
            + "OPEN_WEATHER_API_KEY is not set."
            + Style.RESET_ALL
        )

        return False

    success, api_function = get_api_function(
        table_name
    )

    if not success:

        print(
            Fore.LIGHTRED_EX
            + f"Unable to get API function for {table_name}."
            + Style.RESET_ALL
        )

        if api_function:
            print(api_function)

        return False

    cities_list = clean_cities()

    for city in cities_list:

        print(
            f"\nGetting data for {city}..."
        )

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

        status, api_output = api_function(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if not status:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to retrieve data for {city}."
                + Style.RESET_ALL
            )

            print(api_output)

            continue

        headers = output_headers_list(
            output=api_output
        )

        values = output_values_list(
            output=api_output
        )

        success, data = output_to_dict(
            headers_output=headers,
            values_output=values
        )

        if not success:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to process data for {city}."
                + Style.RESET_ALL
            )

            print(data)

            continue

        success, message = insert_data(
            db_connection=db_connection,
            table_name=table_name,
            data_dict=data
        )

        if not success:

            print(
                Fore.LIGHTRED_EX
                + f"{city} was not inserted."
                + Style.RESET_ALL
            )

            print(message)

            continue

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} imported successfully."
            + Style.RESET_ALL
        )

    print(
        f"\n{table_name} table has been processed."
    )

    return True

def required_table_insert(table_name):

    db_status, db_connection = connection()

    if not db_status:
        return False, db_connection

    if not find_table(
        db_connection=db_connection,
        table_name=table_name
    ):
        return False, (
            f"Table '{table_name}' does not exist. "
            f"Create it first with: "
            f"lastfrontier -c {table_name.replace('_', '-')}"
        )

    config = get_table_config(table_name)

    api_name = config.get("api_func")

    if api_name:

        success = insert_api_table(
            table_name=table_name,
            db_connection=db_connection
        )

    else:

        success = insert_master_table(
            table_name=table_name,
            db_connection=db_connection
        )

    return success, None