import requests
import json #formattings

def masterlist_api():

    api_key = "eca10603a88fdaca04e49b444e603702"
    url = "https://api.legiscan.com/"

    params = {
        "key": api_key,
        "op": "getMasterList",
        "state": "AK"}

    response = requests.get(url, params=params)
    content = response.json()


    print(json.dumps(content, indent=4))

def sessionlist_api():

    api_key = "eca10603a88fdaca04e49b444e603702"
    url = "https://api.legiscan.com/"

    params = {
        "key": api_key,
        "op": "getSessionList",
        "state": "AK"}

    response = requests.get(url, params=params)
    content = response.json()


    print(json.dumps(content, indent=4))


sessionlist_api()
    