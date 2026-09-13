# This .py file acts as a test file during production

import open_weather_api as w
from datetime import datetime


lat = 61.2163
lon = -149.8949
app = "c56045956e647d6e796f18982704d1d2"
print(w.alaska_time_unix())
response = (w.road_risk_api(
    lat=lat,
    lon=lon,
    api_key=app
))
print(response.status_code)
print(response.text)