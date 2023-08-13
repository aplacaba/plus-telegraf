from datetime import datetime, timedelta
import os
import pytz
import requests

API_KEY = os.environ.get("PHOTON_API_KEY")
API_ENDPOINT = os.environ.get("PHOTON_API")
INTERVAL = "1h"
TIME_FORMAT = "%Y-%m-%d %R"

def run_import():
    now = datetime.utcnow()
    params = {
        'start': (now - timedelta(days=1)).strftime(TIME_FORMAT),
        'end': now.strftime(TIME_FORMAT),
        'interval': INTERVAL
    }
    headers = {'X-API-Key': API_KEY}
    req = requests.get(API_ENDPOINT, headers=headers, params=params)
    return req.json()


def format_ts(timestamp):
    naive = datetime.fromisoformat(timestamp)
    local_dt = naive.astimezone(pytz.timezone("Asia/Manila"))
    utc_dt = local_dt.astimezone(pytz.UTC)
    return round(datetime.timestamp(utc_dt))


def line_protocol(data):
    return "photon_data,plant_no={plant_no} energy={energy},irradiance={irradiance} {timestamp}".format(
        plant_no=data["plant_no"],
        energy=data["power"],
        irradiance=data["irradiance"],
        timestamp=format_ts(data["log_timestamp"])
    )


def main():
    result = run_import()
    filtered = filter(lambda x: x.get("power") is not None, result["data"])
    print("\n".join(list(map(line_protocol, filtered))))


if __name__ == "__main__":
    main()
