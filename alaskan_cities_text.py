import open_weather_api as w
from validation import exit_input, valid_input
from colorama import Fore, Back, Style, init
from customizable import delay_print

# Remove whitespaces, remove empty lines in alaskan_cities.txt
def clean_file():
    with open("alaskan_cities.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    with open("alaskan_cities.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

    return lines

# Remove duplicates in file
def remove_duplicates(lines):
    unique_cities = []
    seen = set()

    for city in lines:
        key = city.strip().casefold()

        if key not in seen:
            seen.add(key)
            unique_cities.append(city.title())

    with open("alaskan_cities.txt", "w") as f:
        for city in unique_cities:
            f.write(city + "\n")

    return unique_cities

# Count number of lines in file
def line_count():
    with open("alaskan_cities.txt") as f:
        return sum(1 for _ in f)

# Print lines in file
def print_lines(lines):
    delay_print("\nThis is the list of current cities:")
    for line in lines:
        print(line)

# Remove non-Alaskan cities from file
def remove_invalid_cities(lines):
    for line in lines[:]:
        if not w.city_in_alaska(line):
            lines.remove(line)

    with open("alaskan_cities.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

# Add city to file
def add_city():
    print(Fore.LIGHTBLUE_EX, end="")
    user_city = exit_input("Enter a city in Alaska: " + Style.RESET_ALL).strip()

    while w.city_in_alaska(user_city) is None:
        print(Fore.LIGHTRED_EX, end="")
        print("That city does not exist or is not located in Alaska.")
        user_city =exit_input("Please try another city: " + Style.RESET_ALL).strip()

    with open("alaskan_cities.txt", "a") as file:
        file.write(user_city + "\n")

# Returns list of all cities we want to retrieve weather APIs for
def all_cities_list():
    lines = clean_file()
    remove_invalid_cities(lines)
    lines = remove_duplicates(lines)

    if line_count() == 0:
        print(Fore.LIGHTBLUE_EX, end="")
        print("There are no cities listed. We need to have at least one city in our list.")
        print(Style.RESET_ALL)
        add_city()
        lines = clean_file()

    print_lines(lines)

    while True:
        print(Fore.LIGHTBLUE_EX, end="\n")
        confirm = valid_input(
            "Would you like to add a city (y/n): " + Style.RESET_ALL
        )

        if confirm == "y":
            add_city()

            lines = clean_file()
            lines = remove_duplicates(lines)

            print_lines(lines)

        elif confirm == "n":
            break

    return lines