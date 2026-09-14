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
    import time
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    from geopy.exc import GeocoderRateLimited

    # Create the client/limiter only once
    if not hasattr(alaskan_city_coord, "_safe_client"):
        client = Nominatim(
            user_agent="last_frontier"
        )

        alaskan_city_coord._safe_client = RateLimiter(
            client.geocode,
            min_delay_seconds=2,
            max_retries=2,
            error_wait_seconds=10,
            swallow_exceptions=False
        )

    safe_client = alaskan_city_coord._safe_client

    try:
        city_state_name = f"{city_name}, {state_name}"

        location = safe_client(
            city_state_name,
            timeout=10
        )

        if location is None:
            print(f"Unable to find coordinates for {city_name}.")
            return None

        return {
            "name": city_name,
            "coord": {
                "lat": location.latitude,
                "lon": location.longitude
            }
        }

    except GeocoderRateLimited as e:
        print(f"Rate limited: {e}")

        retry_after = getattr(e, "retry_after", None)

        if retry_after:
            print(f"Waiting {retry_after} seconds...")
            time.sleep(retry_after)

        return None

def alaskan_cities_list(my_list):
    headers_list = func.output_headers_list(output=my_list)
    values_list = func.output_values_list(output=my_list)

    headers_values_list = func.output_to_dict(
        headers_output=headers_list,
        values_output=values_list
    )

    return headers_values_list
