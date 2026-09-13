# This .py file acts as a test file during production

import open_weather_api as w
from datetime import datetime

dt = datetime.now()
unix_ts = dt.timestamp()
print(unix_ts)