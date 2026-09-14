import open_weather_api as w
import sql_server as s
import user_cities as a
import cities_table as ac
import os

from validation import exit_input
from colorama import Fore, Style, init
from customizable import delay_print
from dotenv import load_dotenv

from required_tables import (
    weather_table,
    air_pollution_table,
    cities_table
)

def main():
    init() # intialize colorama
    load_dotenv() # load .env file

    delay_print("Welcome to LastFrontier.")

    user_list = a.all_cities_list()
    head_list = ac.alaskan_cities()

    # Get and validate API key
    while True:

        print(Fore.LIGHTBLUE_EX, end="")

        api_key = os.getenv("OPEN_WEATHER_API_KEY")

        # Test the API key using the first city
        lat, lon = w.lat_and_long(city_name=user_list[0])

        if lat is None or lon is None:
            print(
                Fore.LIGHTRED_EX
                + "Unable to find city coordinates."
                + Style.RESET_ALL
            )
            return 

        status, output = w.current_weather_api(lat=lat, lon=lon, api_key=api_key)

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

        break

    # CONNECT TO POSTGRESQL DATABASE
    delay_print("\nConnecting to database...\n")

    while True:
        user_host = os.getenv("DB_HOST")
        user_db_name = os.getenv("DB_NAME")
        user_name = os.getenv("DB_USER")
        user_password = os.getenv("DB_PASS")
        user_port = os.getenv("DB_PORT")

        status, conn_output = s.connection(
            database=user_db_name,
            username=user_name,
            password=user_password,
            host=user_host,
            port=user_port
        )

        if status is True:
            print(
                Fore.LIGHTGREEN_EX
                +"Connected successfully!"
                + Style.RESET_ALL
            )
            break

        print(
            Fore.LIGHTRED_EX
            + str(conn_output)
            + Style.RESET_ALL
        )
        break

    #TABLE 1: CITIES_TABLE
    success = cities_table(
        db_connection=conn_output,
        cities_list=head_list
    )

    if success is False:
        print(
            Fore.LIGHTRED_EX
            + "Cities table import failed."
            + Style.RESET_ALL
        )
        return

    #TABLE 2: WEATHER_TABLE
    success = weather_table(
        db_connection=conn_output,
        api_key=api_key,
        cities_list=user_list
    )

    if success is False:
        print(
            Fore.LIGHTRED_EX
            + "Weather table import failed."
            + Style.RESET_ALL
        )
        return

    # TABLE 3: AIR POLLUTION TABLE
    success = air_pollution_table(
        db_connection=conn_output,
        api_key=api_key,
        cities_list=user_list
    )

    if success is False:
        print(
            Fore.LIGHTRED_EX
            + "Air pollution table import failed."
            + Style.RESET_ALL
        )
        return

    print(
        Fore.LIGHTGREEN_EX
        + "\nAll data has been imported successfully!"
        + Style.RESET_ALL
    )

    print("\nThank you for interacting with LastFrontier. Goodbye!")

if __name__ == "__main__":
    main()