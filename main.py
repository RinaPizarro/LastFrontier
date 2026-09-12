import open_weather_api as w
import sql_server as s
import alaskan_cities_text as a
from validation import exit_input
from colorama import Fore, Back, Style, init


def main():
    my_list = a.all_cities_list()

    while True:
        print(Fore.LIGHTBLUE_EX, end="")
        api_key = exit_input("Please enter your API Key: " + Style.RESET_ALL)

        lat, lon = w.lat_and_long(city_name=my_list[0])

        status, output = w.current_weather_api(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if status is False:
            print(Fore.LIGHTRED_EX, end="")
            print("That key did not work. Please try a different key.\n" + Style.RESET_ALL)
            continue

        elif status is None:
            print(output)
            return

        else:
            break

    print("\nLet's connect to the LastFrontier database and import our weather information.")

    while True:
        print(Fore.LIGHTBLUE_EX, end="")
        user_host = exit_input("\nEnter host: " + Style.RESET_ALL)

        print(Fore.LIGHTBLUE_EX, end="")
        user_name = exit_input("Enter username: " + Style.RESET_ALL)

        print(Fore.LIGHTBLUE_EX, end="")
        user_password = exit_input("Enter password: " + Style.RESET_ALL)

        status, conn_output = s.connection(
            username=user_name,
            password=user_password,
            host=user_host
        )

        if status is True:
            print(Fore.LIGHTGREEN_EX, end="")
            print("Connected successfully!" + Style.RESET_ALL)
            break

        if status is False:
            print(conn_output)
            print(Fore.LIGHTRED_EX, end="")
            print("Let's try that again." + Style.RESET_ALL)
            continue

        else:
            print(conn_output)
            return

    user_table = exit_input(
        "\nLet's see if our table exists. What is your table name? "
    )
    user_table = user_table.lower()

    # Use the weather data we already retrieved when checking the API key.
    weather_headers = w.output_headers_list(
        output=output
    )

    weather_values = w.output_values_list(
        output=output
    )

    status, weather_dict_output = w.output_to_dict(
        headers_output=weather_headers,
        values_output=weather_values
    )

    if status is False:
        print(weather_dict_output)
        return

    table_exists = s.find_table(
        db_connection=conn_output,
        table_name=user_table
    )

    if table_exists is False:
        status, message = s.create_table(
            db_connection=conn_output,
            table_name=user_table,
            columns_dict=weather_dict_output
        )

        if status is False:
            print(message)
            return

        print(message)

    # Insert weather information for each city.
    for city in my_list:
        print(f"\nGetting weather for {city}...")

        # The first city's weather was already retrieved above.
        if city == my_list[0]:
            weather_data = weather_dict_output

        else:
            lat, lon = w.lat_and_long(city_name=city)

            status, output = w.current_weather_api(
                lat=lat,
                lon=lon,
                api_key=api_key
            )

            if status is False:
                print("That key did not work.\n")
                return

            elif status is None:
                print(output)
                return

            weather_headers = w.output_headers_list(
                output=output
            )

            weather_values = w.output_values_list(
                output=output
            )

            status, weather_data = w.output_to_dict(
                headers_output=weather_headers,
                values_output=weather_values
            )

            if status is False:
                print(weather_data)
                return

        success, message = s.insert_data(
            db_connection=conn_output,
            table_name=user_table,
            data_dict=weather_data
        )

        if success is True:
            print(Fore.LIGHTGREEN_EX, end="")
            print(f"{city} has been inserted into the {user_table} table." + Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX, end="")
            print(f"{city} was not inserted into the {user_table} table." + Style.RESET_ALL)
            print(message)
            return

    print("\nThank you for interacting with LastFrontier. Goodbye!")


if __name__ == "__main__":
    main()