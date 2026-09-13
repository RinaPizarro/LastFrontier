import requests
from country_state_city import City
from geopy.geocoders import Nominatim
from zoneinfo import ZoneInfo


def verify_city(city_name):
    cities = City.get_cities_of_state('US', 'AK')

    for city in cities:
        if city.name.lower() == city_name.lower():
            return city

    return None

def lat_and_long(
        city_name,
        state_name="Alaska"):

    client = Nominatim(
        user_agent="last_frontier"
    )

    city_state_name = f'{city_name}, {state_name}'

    location = client.geocode(
        city_state_name,
        timeout=10
    )

    if location is None:
        return None, None

    return (
        str(location.latitude),
        str(location.longitude)
    )

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

    response = requests.get(
        url,
        params=params
    )

    if response.status_code == 200:
        return True, response.json()

    elif response.status_code == 401:
        return False, "The API key does not work."

    else:
        return None, (
            "Unable to retrieve weather. "
            "Please try again later."
        )

def air_pollution_api(
        lat,
        lon,
        api_key):

    url = (
        "https://api.openweathermap.org/data/2.5/"
        "air_pollution"
    )

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }

    response = requests.get(
        url,
        params=params
    )

    if response.status_code == 200:
        return True, response.json()

    elif response.status_code == 401:
        return False, "The API key does not work."

    else:
        return None, (
            "Unable to retrieve air pollution. "
            "Please try again later."
        )