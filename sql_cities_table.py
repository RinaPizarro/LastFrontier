from country_state_city import City
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderRateLimited

def all_alaskan_cities():
    cities = City.get_cities_of_state('US', 'AK')
    cities_list = []
    for city in cities:
        cities_list.append(city.name)

    return cities_list

def all_alaskan_coord(
    city_list,
    state_name="Alaska"):

    client = Nominatim(
        user_agent="last_frontier"
    )

    safe_client = RateLimiter(client.geocode, min_delay_seconds=1)

    my_list = []

    try:
        for city_name in city_list:

            try: 
                city_dict = {}
                city_state_name = f'{city_name}, {state_name}'

                location = safe_client(
                    city_state_name,
                    timeout=10,
                )

                city_dict["name"] = city_name
                city_dict["coord.lon"] = location.longitude
                city_dict["coord.lan"] = str(location.latitude)
                my_list.append(city_dict)
                print(my_list)

            except AttributeError as a:
                # Skip city_name is coordinates do not exist 
                continue

        return my_list

    
    except GeocoderRateLimited as e:
        print(f"Rate limited: {e}")
        # Optionally wait and retry
        import time
        time.sleep(e.retry_after)
