from lastfrontier.cities_table import all_alaskan_cities, alaskan_city_coord
from lastfrontier.user_cities import all_cities_list
from lastfrontier.open_weather_api import (
    current_weather_api,
    lat_and_long,
    air_pollution_api,
)
from lastfrontier.sql_server import (
    create_or_insert,
    find_existing_row,
    connection,
)
from lastfrontier.column_functions import (
    output_headers_list,
    output_values_list,
    output_to_dict,
)
from colorama import Fore, Style, init
from dotenv import load_dotenv
from pathlib import Path

import os
import json

# REQUIRED TABLES:
# alaskan_cities
# weather
# air_pollution

# This table contains Alaskan cities name, latitude, and longtitude

#TODO SEPERATE MASTER AND FACT TABLES

# Determine table type 
def table_type(table_name):
    FILE_PATH = Path(__file__).resolve().parent / "data" / "tables.json"

    with open(FILE_PATH,'r') as file:
        output = json.load(file)
        table_value = output[table_name]
        return table_value["type"]

def table_api_func(table_name):
    FILE_PATH = Path(__file__).resolve().parent / "data" / "tables.json"

    with open(FILE_PATH,'r') as file:
        output = json.load(file)
        table_value = output[table_name]
        return table_value["api_func"]

def required_table_create(table_name):
    db_status, db_connection = connection()
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    table_message_shown = False

    if table_type(table_name) == "Master":
        cities_list = all_alaskan_cities(count=1)
        columns_list = output_headers_list(cities_list)
        return cities_list
        
    if table_type(table_name) == "Fact":
        cities_list = all_cities_list()

        for city in cities_list:
            pass
        
    else:
        return # stop the program 

print(required_table_create("alaskan_cities"))