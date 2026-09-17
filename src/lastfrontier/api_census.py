import os
import requests 

#TODO 
api_key = os.getenv("CENSUS_API")

# Time Series Current Population Survey
def poverty_api(
    api_key="f5b9a4d1cf2b008dbffb654a0275b544a966d2a1",
    ):

    url = "http://api.census.gov/data/timeseries/poverty/histpov2"

    params = {"key": api_key, "time": 2018}

    response = requests.get(url, params=params)
    print(response)

    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        return None, "Unable to retrieve wildfire incidents. Please try again later."

status, message = poverty_api()
print(status)