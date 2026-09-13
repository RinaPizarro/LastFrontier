# This .py file acts as a test file during production

import open_weather_api as w
from datetime import datetime


lat = 61.2163
lon = -149.8949
app = ""
print(w.alaska_time_unix())

status, message = w.air_pollution_api(lat,lon,app)
print(message)