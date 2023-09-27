import os, requests

API_KEY = os.environ.get("PHOTON_API_KEY")

class PhotonImporter:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def execute(self, start, end, interval):
        params = {
            'start': start,
            'end': end,
            'interval': interval
        }

        headers = {'X-API-Key': API_KEY}
        req = requests.get(self.endpoint, headers=headers, params=params)
        return req.json()
    
