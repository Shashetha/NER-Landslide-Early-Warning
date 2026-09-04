import json
import requests

URL = "https://disc.gsfc.nasa.gov/service/subset/jsonwsp"

payload = {
    "methodname": "subset",
    "type": "jsonwsp/request",
    "version": "1.0",
    "args": {
        "role": "subset",
        "start": "2013-07-12T00:00:00",
        "end": "2013-07-12T23:59:59",
        "box": [88.0, 22.0, 97.5, 29.5],
        "crop": True,
        "data": [
            {
                "datasetId": "GPM_3IMERGDF",
                "variable": "precipitation"
            }
        ]
    }
}

response = requests.post(
    URL,
    json=payload,
    timeout=120
)

print("HTTP status:", response.status_code)
print("\nResponse:")
print(json.dumps(response.json(), indent=2))