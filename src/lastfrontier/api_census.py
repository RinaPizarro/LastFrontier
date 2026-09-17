import os
import requests 

#TODO 
api_key = os.getenv("CENSUS_API")

# Time Series Current Population Survey
def acs_1_year_api(
    api_key,
    ):

    url = "http://api.census.gov/data/2024/acs/acs1"

    params = {
        "get": "NAME",
        "for": "state:02",
        "key": api_key
    }

    response = requests.get(url, params=params)
    print(response)

    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        return None, "Unable to retrieve wildfire incidents. Please try again later."

status, message = acs_1_year_api()
print(status)
print(message)