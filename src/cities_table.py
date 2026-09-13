from country_state_city import City
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderRateLimited

import column_functions as func
import sql_server as s

def alaskan_cities():
    cities = City.get_cities_of_state('US', 'AK')
    cities_list = []

    for city in cities:
        cities_list.append(city.name)

    return cities_list

def alaskan_city_coord(
    city_name,
    state_name="Alaska"
    ):

    client = Nominatim(user_agent="last_frontier")

    safe_client = RateLimiter(client.geocode, min_delay_seconds=1)

    try:
        city_state_name = f"{city_name}, {state_name}"

        location = safe_client(city_state_name, timeout=10)

        if location is None:
            return None

        city_dict = {
            "name": city_name,
            "coord": {
                "lat": location.latitude,
                "lon": location.longitude
            }
        }

        return city_dict

    except AttributeError:
        # Coordinates do not exist
        return None

    except GeocoderRateLimited as e:
        print(f"Rate limited: {e}")

        import time
        time.sleep(e.retry_after)

        return None

def alaskan_cities_list(my_list):
    headers_list = func.output_headers_list(output=my_list)
    values_list = func.output_values_list(output=my_list)

    headers_values_list = func.output_to_dict(
        headers_output=headers_list,
        values_output=values_list
    )

    return headers_values_list