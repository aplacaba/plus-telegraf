from datetime import datetime, timedelta
import os
import sys
import pytz
import requests

API_KEY = os.environ.get("PHOTON_API_KEY")
API_ENDPOINT = os.environ.get("PHOTON_API")
TIME_FORMAT = "%Y-%m-%d %R"
NANOSECONDS = 1_000_000_000
INTERVAL = sys.argv[1]

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
    return int(datetime.fromisoformat(timestamp).timestamp()) * NANOSECONDS


def hourly_line_protocol(data):
    return "hourly_photon_data,plant_no={plant_no} energy={energy},irradiance={irradiance} {timestamp}".format(
        plant_no=data["plant_no"],
        energy=data["power"],
        irradiance=data["irradiance"],
        timestamp=format_ts(data["log_timestamp"])
    )


def daily_line_protocol(data):
    return "daily_photon_data,plant_no={plant_no} energy={energy},irradiance={irradiance} {timestamp}".format(
        plant_no=data["plant_no"],
        energy=data["energy"],
        irradiance=data["irradiation"],
        timestamp=format_ts(data["log_timestamp"])
    )


def output_kw_line_protocol(data):
    return "photon_output_kw,inverter_id={inverter_id} output_kw={output_kw} {timestamp}".format(
        inverter_id=data["device_no"],
        output_kw=data["output_kw"],
        timestamp=format_ts(data["log_timestamp"])
    )


def main():
    result = run_import()

    if INTERVAL == "1h":
        filtered = filter(lambda x: x.get("power") is not None, result["data"])
        print("\n".join(list(map(hourly_line_protocol, filtered))))

    elif INTERVAL == "1d":
        print("\n".join(list(map(daily_line_protocol, result["data"]))))

    elif INTERVAL == "15m":
        print("\n".join(list(map(output_kw_line_protocol, result["data"]))))


if __name__ == "__main__":
    main()
