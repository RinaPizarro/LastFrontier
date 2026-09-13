# This .py file acts as a test file during production

import src.open_weather_api as w
from datetime import datetime
import src.alaskan_cities_table as ss
import src.list_functions as func

lat = 61.2163
lon = -149.8949

print(ss.all_alaskan_cities())
print(ss.all_alaskan_coord(ss.all_alaskan_cities()[0]))