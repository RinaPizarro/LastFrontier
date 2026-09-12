import open_weather_api as w
import sql_server as s
import alaskan_cities_text as a
from validation import exit_input

def main():
    my_list = a.all_cities_list()

    while True:
        api_key = exit_input("Please enter your API Key: ")

        lat, lon = w.lat_and_long(city_name=my_list[0])

        status, output = w.current_weather_api(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if status is False:
            print("That key did not work. Please try a different key.")
            continue

        elif status is None:
            print(output)
            return

        else:
            break

    print("\nLet's connect to the LastFrontier database and import our weather information.")

    while True:
        user_host = exit_input("\nEnter host: ")
        user_name = exit_input("Enter username: ")
        user_password = exit_input("Enter password: ")

        status, conn_output = s.connection(
            username=user_name,
            password=user_password,
            host=user_host
        )

        if status is True:
            print("Connected successfully!")
            break

        if status is False:
            print(conn_output)
            print("Let's try that again.")
            continue

        else:
            print(conn_output)
            return

    user_table = exit_input("\nLet's see if our table exists. What is your table name? ")
    user_table = user_table.lower()

    city = my_list[0]

    lat, lon = w.lat_and_long(city_name=city)

    status, output = w.current_weather_api(
        lat=lat,
        lon=lon,
        api_key=api_key
    )

    if status is False:
        print("That key did not work.")
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

    for city in my_list:
        print(f"\nGetting weather for {city}...")

        lat, lon = w.lat_and_long(city_name=city)

        status, output = w.current_weather_api(
            lat=lat,
            lon=lon,
            api_key=api_key
        )

        if status is False:
            print("That key did not work.")
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

        status, weather_dict_output = w.output_to_dict(
            headers_output=weather_headers,
            values_output=weather_values
        )

        if status is True:
            success, message = s.insert_data(
                db_connection=conn_output,
                table_name=user_table,
                data_dict=weather_dict_output
            )

            if success is True:
                print(f"{city} has been inserted into the {user_table} table.")
            else:
                print(f"{city} was not inserted into the {user_table} table.")
                print(message)
                return

        else:
            print(weather_dict_output)
            return

    print("\nThank you for interacting with LastFrontier. Goodbye!")

if __name__ == "__main__":
    main()