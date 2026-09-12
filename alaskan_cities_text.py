import open_weather_api as w
import validation as val

# Remove whitespaces, remove empty lines in alaska_cities.txt
def clean_file():
    with open('alaskan_cities.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    with open('alaskan_cities.txt', 'w') as f:
        for line in lines:
            f.write(line + '\n')

    return lines # return current list of cities

# Count number of lines in file
def line_count():
    with open('alaskan_cities.txt') as f:
        return sum(1 for _ in f)

# Print lines in file
def print_lines(lines):
    print("This is the list of current cities:")
    for line in lines:
        print(line)

# Remove non Alaskan cities from file
def remove_invalid_cities(lines):
    for line in lines[:]:
        if not w.city_in_alaska(line):
            lines.remove(line)

    with open('alaskan_cities.txt', 'w') as f:
        for line in lines:
            f.write(line + '\n')

# Add city to file
def add_city():
    user_city = input("Enter a city in Alaska: ")
    
    while w.city_in_alaska(user_city) is None:
        user_city = input("That city does not exist or is not located in Alaska. Please try another city: ")

    with open("alaskan_cities.txt", "a") as file:
        file.write(f'{user_city}\n')

# Returns list of all cities we want to retrieve weather APIs for
def final_cities_list():
    lines = a.clean_file()
    a.remove_invalid_cities(lines)
    
    if a.line_count() == 0:
        print("There are no cities listed. Go ahead and add a city. ")
    else:
        a.print_lines(lines=lines)
        pass #TODO