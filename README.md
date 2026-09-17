# LastFrontier

LastFrontier is a data-ingestion program that retrieves data from OpenWeather and the Alaska GeoPortal and stores the collected data in a database. It provides a centralized way to acquire, organize, and persist weather and geospatial data for downstream analysis and applications. 

## Libraries
- pip install reqeusts
- pip install geopy
- pip install country_state_city
- pip install psycopg2 
- pip install python-dotenv
- import json
- import datetime
- import zoneinfo
- import time
- import sys

## Files Explained
### alaskan_cities.txt
This file contains the list of all cities expected to be used when retrieving weather data from the API. alaskan_cities_text.py allows users to add cities to the file, but does not allow users to remove cities. This would need to be done manually until implentation.

## .Env
1. Copy .env.example to .env
2. Add your API keys to .env
3. Run the program

## Resources
https://openweathermap.org/api/current?collection=current_forecast
https://511.alaska.gov/developers/doc
https://www2.census.gov/data/api-documentation/api-user-guide.pdf