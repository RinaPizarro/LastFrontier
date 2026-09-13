from country_state_city import City
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


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

    my_dict = {}

    for city_name in city_list:
        city_state_name = f'{city_name}, {state_name}'

        location = client.geocode(
            city_state_name,
            timeout=10,
        )

        if location is None:
            return None, None

        my_dict["name"] = city_name
        my_dict["coord.lon"] = str(location.longitude)
        my_dict["coord.lan"] = str(location.latitude)

    return my_dict