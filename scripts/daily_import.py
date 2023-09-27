from photon import PhotonImporter
from time_helper import format_ts, time_params
import os

API_ENDPOINT = os.environ.get("PHOTON_API")
INTERVAL = "1d"

def line_protocol(data):
    return "daily_photon_data,plant_no={plant_no} energy={energy},irradiance={irradiance} {timestamp}".format(
        plant_no=data["plant_no"],
        energy=data["energy"],
        irradiance=data["irradiation"],
        timestamp=format_ts(data["log_timestamp"])
    )
    
def main():
    photon = PhotonImporter(API_ENDPOINT)
    params = time_params()
    result = photon.execute(params["start"], params["end"], INTERVAL)
    print("\n".join(list(map(line_protocol, result["data"]))))

if __name__ == "__main__":
    main()
