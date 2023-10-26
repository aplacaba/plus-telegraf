from photon import PhotonImporter
from time_helper import format_ts, time_params
import os

API_ENDPOINT = os.environ.get("INVERTER_PHOTON_API")
INTERVAL = "15m"

def line_protocol(data):
    return "photon_output_kw,inverter_id={inverter_id} output_kw={output_kw} {timestamp}".format(
        inverter_id=data["device_no"],
        output_kw=data["output_kw"],
        timestamp=format_ts(data["log_timestamp"])
    )


def main():
    photon = PhotonImporter(API_ENDPOINT)
    params = time_params(2)
    result = photon.execute(params["start"], params["end"], INTERVAL)
    filtered = filter(lambda x: x.get("output_kw") is not None, result["data"])
    print("\n".join(list(map(line_protocol, filtered))))

if __name__ == "__main__":
    main()
