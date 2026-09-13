import open_weather_api as w
import sql_server as s
import alaskan_cities_text as a

from validation import exit_input
from colorama import Fore, Style, init
from customizable import delay_print, loading_city_animation

def main():

    init()

    delay_print(
        "Welcome to LastFrontier. "
        "Let's begin by importing the weather into our database."
    )

    my_list = a.all_cities_list()

    while True:

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        api_key = exit_input(
            "Please enter your API Key: "
            + Style.RESET_ALL
        )

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

    for city in my_list:

        print(
            Fore.LIGHTBLUE_EX,
            end=""
        )

        print(
            f"\nGetting data for {city}..."
            + Style.RESET_ALL
        )

        lat, lon = w.lat_and_long(
            city_name=city
        )

        if lat is None or lon is None:

            print(
                Fore.LIGHTRED_EX
                + f"Unable to find coordinates for {city}."
                + Style.RESET_ALL
            )

            continue

        status, weather_output = w.current_weather_api(
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

            return

        elif status is None:

            print(weather_output)
            return

        weather_headers = w.output_headers_list(
            output=weather_output
        )

        weather_values = w.output_values_list(
            output=weather_output
        )

        status, weather_data = w.output_to_dict(
            headers_output=weather_headers,
            values_output=weather_values
        )

        if status is False:

            print(weather_data)
            return

        status, pollution_output = w.air_pollution_api(
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

            return

        elif status is None:

            print(pollution_output)
            return

        pollution_headers = w.output_headers_list(
            output=pollution_output
        )

        pollution_values = w.output_values_list(
            output=pollution_output
        )

        status, pollution_data = w.output_to_dict(
            headers_output=pollution_headers,
            values_output=pollution_values
        )

        if status is False:

            print(pollution_data)
            return

        success, message = loading_city_animation(
            city,
            lambda: s.create_or_insert(
                db_connection=conn_output,
                table_name="weather",
                data_dict=weather_data
            )
        )

        if success is False:

            print(
                Fore.LIGHTRED_EX
                + f"{city} weather was not inserted."
                + Style.RESET_ALL
            )

            print(message)
            return

        success, message = s.create_or_insert(
            db_connection=conn_output,
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
            return

        print(
            Fore.LIGHTGREEN_EX
            + f"{city} has been imported successfully."
            + Style.RESET_ALL
        )

    print("\nThank you for interacting with LastFrontier. Goodbye!")


if __name__ == "__main__":
    main()