import open_weather_api as w
import sql_server as s
import user_alaskan_cities as a
import alaskan_cities_table as ac

from validation import exit_input
from colorama import Fore, Style, init
from customizable import delay_print

from required_tables import (
    weather_table,
    air_pollution_table,
    cities_table
)

def main():

    init()

    delay_print(
        "Welcome to LastFrontier. "
        "Let's begin by importing the weather into our database."
    )

    my_list = a.all_cities_list()
    all_list = ac.alaskan_cities()

    # Get and validate API key

    while True:

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        api_key = exit_input(
            "Please enter your API Key: "
            + Style.RESET_ALL
        )

        # Test the API key using the first city
        lat, lon = w.lat_and_long(
            city_name=my_list[0]
        )

        if lat is None or lon is None:

            print(
                Fore.LIGHTRED_EX
                + "Unable to find city coordinates."
                + Style.RESET_ALL
            )

            return

        status, output = w.current_weather_api(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if status is False:

            print(
                Fore.LIGHTRED_EX
                + "That key did not work. "
                "Please try a different key.\n"
                + Style.RESET_ALL
            )

            continue

        elif status is None:

            print(output)
            return

        break

    delay_print(
        "\nLet's connect to the LastFrontier database "
        "and import our weather information."
    )

    while True:

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        user_host = exit_input(
            "\nEnter host: "
            + Style.RESET_ALL
        )

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        user_name = exit_input(
            "Enter username: "
            + Style.RESET_ALL
        )

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        user_password = exit_input(
            "Enter password: "
            + Style.RESET_ALL
        )

        status, conn_output = s.connection(
            username=user_name,
            password=user_password,
            host=user_host
        )

        if status is True:

            print(
                Fore.LIGHTGREEN_EX
                + "Connected successfully!"
                + Style.RESET_ALL
            )

            break

        print(
            Fore.LIGHTRED_EX
            + str(conn_output)
            + Style.RESET_ALL
        )

        print(
            Fore.LIGHTRED_EX
            + "Let's try that again."
            + Style.RESET_ALL
        )

    success = cities_table(
        db_connection=conn_output,
        cities_list=all_list
    )

    if success is False:

        print(
            Fore.LIGHTRED_EX
            + "Cities table import failed."
            + Style.RESET_ALL
        )

        return

    success = weather_table(
        db_connection=conn_output,
        api_key=api_key,
        cities_list=my_list
    )

    if success is False:

        print(
            Fore.LIGHTRED_EX
            + "Weather table import failed."
            + Style.RESET_ALL
        )

        return

    success = air_pollution_table(
        db_connection=conn_output,
        api_key=api_key,
        cities_list=my_list
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

    print(
        "\nThank you for interacting with LastFrontier. Goodbye!"
    )


if __name__ == "__main__":
    main()