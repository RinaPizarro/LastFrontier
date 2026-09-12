import open_weather_api as w
import sql_server as s

def main():
    user_city = input("Enter a city in Alaska: ")

    # Validate city
    while w.city_in_alaska(user_city) is None:
        user_city = input("That city does not exist or is not located in Alaska. Please try another city: ")

    lat, lon = w.lat_and_long(city_name=user_city)

    # Validate API key and get weather
    while True:
        api_key = input("Please enter your API Key: ")

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
            return  # Stop the entire program

        else:
            break

    print(f'\nHere is the weather for {user_city.capitalize()}. Units are in Imperial:')
    weather_headers = w.output_headers_list(output=output)
    weather_values = w.output_values_list(output=output)
    status, weather_dict_output = w.output_to_dict(headers_output=weather_headers, values_output=weather_values)
    
    if status == True:
        for key, value in weather_dict_output.items():
            print(f'{key}: {value}')
    else:
        print(weather_dict_output)
        return # stop program

    print("\nLet's connect to the LastFrontier database and import our weather information.")
    while True:
        user_host = input("\nEnter host: ")
        user_name = input("Enter username: ")
        user_password = input("Enter password: ")

        status, conn_output = s.connection(
            username=user_name,
            password=user_password,
            host=user_host)

        if status == True:
            print("Connected successfully!")
            break
        if status == False:
            print(conn_output)
            print("Let's try that again. ")
            continue
        else:
            print(conn_output)
            return # stop the program

    user_table = input("\nLet's create our table. What is your table name? ")

    while True:
        status, message = s.create_table(db_connection=conn_output, table_name=user_table, columns_dict=weather_dict_output)
        if status == True:
            break
        else:
            print(message)
            return # stop the program

    print("Thank you for interacting with LastFrontier. Goodbye!")

if __name__ == "__main__":
    main()