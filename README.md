# LastFrontier

LastFrontier is a data-ingestion program that retrieves data from OpenWeather and the Alaska GeoPortal and stores the collected data in a database. It provides a centralized way to acquire, organize, and persist weather and geospatial data for downstream analysis and applications. 

## Libraries
- pip install reqeusts
- pip install geopy
- pip install country_state_city
- pip install psycopg2 
- import json
- import datetime
- import zoneinfo
- import time
- import sys

## Files Explained
### alaskan_cities.txt
This file contains the list of all cities expected to be used when retrieving weather data from the API. 