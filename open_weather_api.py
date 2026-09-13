import requests
from country_state_city import City
from geopy.geocoders import Nominatim
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def city_in_alaska(city_name):
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


def universal_time():
    universal_time = datetime.now(timezone.utc)

    return universal_time.isoformat(
        timespec="seconds"
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


def output_headers_list(output):
    columns_headers = []

    columns_headers.append("time_utc")

    for key, value in output.items():

        if isinstance(value, dict):

            for nested_key, nested_value in value.items():

                if isinstance(nested_value, dict):

                    for sub_key in nested_value.keys():
                        columns_headers.append(
                            f"{key}.{nested_key}.{sub_key}"
                        )

                else:
                    columns_headers.append(
                        f"{key}.{nested_key}"
                    )

        elif isinstance(value, list):

            for item in value:

                if isinstance(item, dict):

                    for nested_key, nested_value in item.items():

                        if isinstance(nested_value, dict):

                            for sub_key in nested_value.keys():
                                columns_headers.append(
                                    f"{key}.{nested_key}.{sub_key}"
                                )

                        else:
                            columns_headers.append(
                                f"{key}.{nested_key}"
                            )

        else:
            columns_headers.append(key)

    return columns_headers

def output_values_list(output):
    column_values = []

    column_values.append(
        universal_time()
    )

    for value in output.values():

        if isinstance(value, dict):

            for nested_value in value.values():

                if isinstance(nested_value, dict):
                    column_values.extend(
                        nested_value.values()
                    )
                else:
                    column_values.append(
                        nested_value
                    )

        elif isinstance(value, list):

            for item in value:

                if isinstance(item, dict):

                    for nested_value in item.values():

                        if isinstance(nested_value, dict):
                            column_values.extend(
                                nested_value.values()
                            )
                        else:
                            column_values.append(
                                nested_value
                            )

        else:
            column_values.append(value)

    return column_values

def output_to_dict(headers_output, values_output):

    if len(headers_output) != len(values_output):
        return (
            False,
            "There is not enough values "
            "for the existing columns."
        )

    my_dict = dict(
        zip(
            headers_output,
            values_output
        )
    )

    return True, my_dict
