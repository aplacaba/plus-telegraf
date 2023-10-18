from photon import PhotonImporter
from time_helper import format_ts, time_params
import os

API_ENDPOINT = os.environ.get("PHOTON_API")
INTERVAL = "1h"

def line_protocol(data):
    return "hourly_photon_data,plant_no={plant_no} energy={energy},irradiance={irradiance} {timestamp}".format(
        plant_no=data["plant_no"],
        energy=data["power"],
        irradiance=data["irradiance"],
        timestamp=format_ts(data["log_timestamp"])
    )

def main():
    photon = PhotonImporter(API_ENDPOINT)
    coverage = 5
    params = time_params(coverage)
    result = photon.execute(params["start"], params["end"], INTERVAL)
    filtered = filter(lambda x: x.get("power") is not None, result["data"])
    print("\n".join(list(map(line_protocol, filtered))))

if __name__ == "__main__":
    main()
