import urllib.request
import json

req = urllib.request.urlopen("http://127.0.0.1:8000/api/v1/gis/risk-zones")
data = json.loads(req.read().decode("utf-8"))

print(f"Total GIS Features on Map: {len(data['features'])}")

live_count = sum(1 for f in data["features"] if f["properties"].get("type") == "LIVE_MONITORING_STATION")
hist_count = sum(1 for f in data["features"] if f["properties"].get("type") == "HISTORICAL_LANDSLIDE")

print(f" - Live Telemetry Monitoring Stations: {live_count}")
print(f" - Real NASA Historical Landslide Events: {hist_count}")
