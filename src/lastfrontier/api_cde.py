import requests
import json

#FBI CDE
def arrest(api_key):
    url = "https://api.usa.gov/crime/fbi/cde/arrest/state/AK/all"

    params = {
        "type": "totals",
        "from": "07-2026",
        "to": "08-2026",
        "API_KEY": api_key
    }
    response = requests.get(url, params=params)

    return response.json()

print(arrest())