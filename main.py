import open_weather_api as w
import sql_server as s

def main():
    user_city = input("Enter a city in Alaska: ")

    # Validate city
    while w.city_in_alaska(user_city) is None:
        user_city = input(
            "That city does not exist or is not located in Alaska. "
            "Please try another city: "
        )

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

    print("Let's connect to the LastFrontier database.")
    while True:
        user_host = input("Enter host: ")
        user_name = input("Enter username: ")
        user_password = input("Enter password: ")

        status, message = s.connection(
            username=user_name,
            password=user_password,
            host=user_host)

        if status == False:
            print(message)
            print("Let's try that again. ")
            continue
        else:
            print(message)
            return # stop the program

    print("Thank you for interacting with LastFrontier. Goodbye!")

if __name__ == "__main__":
    main()