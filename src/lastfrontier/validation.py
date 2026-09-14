# Module for validating user input
import sys
import os

from dotenv import load_dotenv
from lastfrontier.open_weather_api import current_weather_api, lat_and_long
from colorama import Fore, Back, Style, init
from country_state_city import City

def valid_weather_api_key():
    api_key = os.getenv("OPEN_WEATHER_API_KEY")

    # Test the API key using the first city
    lat, lon = lat_and_long(city_name="Anchorage")
    
    status, output = current_weather_api(lat=lat, lon=lon, api_key=api_key)

    if status is False:
        print(
            Fore.LIGHTRED_EX
            + "That key did not work. Please verify your Open Weather API key.\n"
            + Style.RESET_ALL
        )
        return

    elif status is None:
        print(output)
        return

    return api_key

def verify_city(city_name):
    cities = City.get_cities_of_state('US', 'AK')

    for city in cities:
        if city.name.lower() == city_name.lower():
            return city

    return None

def valid_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()

        if user_input == "exit":
            sys.exit()

        elif user_input == "y":
            return "y"

        elif user_input == "n":
            return "n"

        else:
            print(Fore.LIGHTRED_EX + "That is not a valid input. Please try again.\n" + Style.RESET_ALL)

# Input is Exit
def exit_input(user_input):
    user_input = input(user_input).strip()

    if user_input.lower() == "exit":
        print(
            "\nThank you for using the Data.gov dataset importer. Goodbye!"
        )
        sys.exit(0)

    return user_input
