import requests

def traffic_events_api(
    api_key,
    format="json"):

    url = "https://511.alaska.gov/api/v2/get/event"

    params = params = {"key": api_key, "format": format}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        return None, "Unable to retrieve weather. Please try again later."


status, message = traffic_events_api()