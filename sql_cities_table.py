from country_state_city import City
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderRateLimited

import list_functions as func

def all_alaskan_cities():
    cities = City.get_cities_of_state('US', 'AK')
    cities_list = []
    for city in cities:
        cities_list.append(city.name)

    return cities_list

#FIXME This needs to be a dictionary not a list
def all_alaskan_coord(
    city_list,
    state_name="Alaska"
):

    client = Nominatim(
        user_agent="last_frontier"
    )

    safe_client = RateLimiter(
        client.geocode,
        min_delay_seconds=1
    )

    full_dict = {}

    try:
        for city_name in city_list:

            try:
                city_state_name = f"{city_name}, {state_name}"

                location = safe_client(
                    city_state_name,
                    timeout=10,
                )

                city_dict = {
                    "name": city_name,
                    "coord": {
                        "lon": location.longitude,
                        "lat": location.latitude
                    }
                }

                full_dict[city_name] = city_dict

                print(full_dict)

            except AttributeError:
                # Skip city_name if coordinates do not exist
                continue

        return full_dict
    
    except GeocoderRateLimited as e:
        print(f"Rate limited: {e}")
        # Optionally wait and retry
        import time
        time.sleep(e.retry_after)

def alaskan_list(my_list):
    headers_list = func.output_headers_list(output=my_list)
    values_list = func.output_values_list(output=my_list)
    headers_values_list = func.output_to_dict(headers_output=headers_list,values_output=values_list)

    return headers_list