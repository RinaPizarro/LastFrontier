# This .py file acts as a test file during production

import open_weather_api as w
from datetime import datetime
import sql_cities_table as ss

lat = 61.2163
lon = -149.8949

print(ss.all_alaskan_cities())
print(ss.all_alaskan_coord(city_list=ss.all_alaskan_cities()))