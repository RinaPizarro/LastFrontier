
# Endpoints: Current Weather Data, Weather Alert Detailed Information

import requests
import json
from geopy.geocoders import Nominatim
from country_state_city import Country, State, City

# Check if city is in Alaska
def city_in_alaska(city_name):
    cities = City.get_cities_of_state('US', 'AK')

    for city in cities:
        if city.name.lower() == city_name.lower():
            return city

    return None

# Return latitude and longtitude of city
def lat_and_long(
        city_name,
        state_name="Alaska"): 
    
    client = Nominatim(user_agent="last_frontier")
    city_state_name = f'{city_name}, {state_name}'
    location = client.geocode(city_state_name, timeout=10).raw

    return str(location["lat"]), str(location["lon"])

# make HTTP request for Open Weather API
def current_weather_api(
        lat, 
        lon, 
        api_key,
        units="Imperial",
        lang="en"): 

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
        "lang": lang
    }

    response = requests.get(url,params)
    if response.status_code == 200:
        json_format = response.json()
        return True, json_format
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        return None, "Unable to retrieve weather. Please try again later."

# turns JSON output from current_weather_api() to list of headers
def output_headers_list(output):
    columns_headers = []

    for i in output:
        if isinstance(output[i], dict):
            keys_list = list(output[i].keys())
            for key in keys_list:
                columns_headers.append(f'{i}.{key}')
        elif isinstance(output[i], list):
            for j in range(len(output[i])):
                if isinstance(output[i][j], dict):
                    keys_list = list(output[i][j].keys())
                    for key in keys_list:
                        columns_headers.append(f'{i}.{key}')
        else:
            columns_headers.append(f'{i}')

    return columns_headers

# map column headers to values from JSON
def output_values_list(output):
    column_values = []

    for value in output.values():
        if isinstance(value, dict):
            column_values.extend(value.values())

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    column_values.extend(item.values())

        else:
            column_values.append(value)

    return column_values

def output_to_dict(headers_output, values_output):
    my_dict = {}

    if len(headers_output) != len(values_output):
        return None, "There is not enough values for the existing columns."
    else:
        for i in headers_output:
            for j in values_output:
                my_dict[i] = j

    return True, my_dict