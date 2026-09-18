import requests
import json
from lastfrontier.validation import valid_month, valid_year

def date_param():
    while True:
        user_month = input("Enter month: ")
        user_year = input("Enter year: ")
        is_valid_month = valid_month(user_month)
        is_valid_year = valid_year(user_year)

        if not is_valid_month or not is_valid_year:
            print("Invalid inputs. Try again.\n")
            continue
        break

    return str(is_valid_month) + "-" + str(is_valid_year)

#FBI CDE
def arrest_api(api_key):
    url = "https://api.usa.gov/crime/fbi/cde/arrest/state/AK/all"

    dates = date_param()

    params = {
        "type": "totals",
        "from": dates,
        "to": dates,
        "API_KEY": api_key
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        content = response.json()
        content["Record Date"] = dates
        return True, content

def homocide_api(api_key):
    url = "https://api.usa.gov/crime/fbi/cde/shr/state/AK"

    dates = date_param()

    params = {
        "type": "totals",
        "from": dates,
        "to": dates,
        "API_KEY": api_key
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, "The API key does not work."
    else:
        content = response.json()
        content["Record Date"] = dates
        return True, content