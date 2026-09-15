# Module for handling alaska_cities.txt file

import lastfrontier.open_weather_api as w
from lastfrontier.validation import exit_input, valid_input, verify_city
from lastfrontier.customizable import delay_print
from pathlib import Path
import os

# Relative file path
FILE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "user_alaskan_cities.txt"
)

# Remove whitespaces, remove empty lines in user_data\user_alaskan_cities.txt
def clean_file():
    with open(FILE_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    with open(FILE_PATH, "w") as f:
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

    with open(FILE_PATH, "w") as f:
        for city in unique_cities:
            f.write(city + "\n")

    return unique_cities

# Count number of lines in file
def line_count():
    with open(FILE_PATH) as f:
        return sum(1 for _ in f)

# Print lines in file
def print_lines(lines):
    delay_print("\nThis is the list of current cities:\n")
    for line in lines:
        print(line)

# Remove non-Alaskan cities from file
def remove_invalid_cities(lines):
    for line in lines[:]:
        if not verify_city(line):
            lines.remove(line)

    with open(FILE_PATH, "w") as f:
        for line in lines:
            f.write(line + "\n")

# Add city to file
def update_list():
    lines = clean_file()

    if line_count() == 0:
        print("There are no cities listed. We need to have at least one city in our list.")

        while True:
            user_city = exit_input("Enter a city in Alaska: ").strip()

            if verify_city(user_city) is not None:
                break

            print("That city does not exist or is not located in Alaska.")

        with open(FILE_PATH, "a") as file:
            file.write(user_city + "\n")

        lines = clean_file()

    print_lines(lines)

    while True:
        confirm = valid_input("\nWould you like to add a city (y/n): ")

        if confirm == "n":
            break

        user_city = exit_input("Enter a city in Alaska: ").strip()

        while verify_city(user_city) is None:
            print("That city does not exist or is not located in Alaska.")
            user_city = exit_input("Please try another city: ").strip()

        with open(FILE_PATH, "a") as file:
            file.write(user_city + "\n")

        lines = clean_file()
        lines = remove_duplicates(lines)

        print_lines(lines)

    return lines

# Returns list of all cities we want to retrieve weather APIs for
def all_cities_list(limit: int = None):
    lines = clean_file()
    remove_invalid_cities(lines)
    lines = remove_duplicates(lines)

    if limit == None:
        return lines
    else:
        return lines[:limit]