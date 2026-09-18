import requests
import json
from datetime import date
import base64
import zipfile
import os

current_year = (date.today()).year

#TODO
#STATUS: ERROR IF SET IS EMPTY
def dataset_list_api(api_key):
    url = "https://api.legiscan.com/"
    params = {
        "key": api_key,
        "op": "getDatasetList",
        "state": "AK",
        "year": current_year
        }

    response = requests.get(url,params)
    return response.json()

def get_dataset_api(api_key):
    url = "https://api.legiscan.com/"

    content = dataset_list_api()

    if content["status"] == "OK":
        keys = content["datasetlist"][0]
        session_id = keys["session_id"]
        access_key = keys["access_key"]
    
        params = {
            "key": api_key,
            "op": "getDataset",
            "id": session_id,
            "access_key": access_key,
            "format": "json"
            }

        response = requests.get(url,params)
        content = response.json()
        return content["dataset"]
    else:
        return None

def unpack_zip():

    folder = "src\\lastfrontier\\data"
    filename = "Alaska_2025_2026.zip"

    file_path = os.path.join(folder, filename)

    os.makedirs(folder, exist_ok=True)

    content = get_dataset_api()

    zip_content = content["zip"]
    zip_data = base64.b64decode(zip_content)

    with open(file_path, "wb") as file:
        file.write(zip_data)

    with zipfile.ZipFile(file_path, "r") as zip_file:
        zip_file.extractall(folder)

    print(f"Saved and extracted to: {folder}")

unpack_zip()