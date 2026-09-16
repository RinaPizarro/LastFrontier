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
        return None, "Unable to retrieve traffic events. Please try again later."

def road_conditions_api(
    api_key,
    format="json"):

    url = "https://511.alaska.gov/api/v3/get/winterroads"

    params = params = {"key": api_key, "format": format}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        return None, "Unable to retrieve road conditions. Please try again later."