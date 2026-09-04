import pandas as pd
import xarray as xr

# --------------------------------------------------
# 1. Load our landslide event list
# --------------------------------------------------

events_file = "data/processed/rainfall_event_list.csv"

events = pd.read_csv(events_file)

events["event_date"] = pd.to_datetime(events["event_date"])

# Take the first landslide event
event = events[events["event_date"] == "2013-07-12"].iloc[0]
print("=" * 60)
print("SINGLE LANDSLIDE RAINFALL TEST")
print("=" * 60)

print("\nLandslide event:")
print(f"Event ID : {event['event_id']}")
print(f"Date     : {event['event_date'].date()}")
print(f"State    : {event['state']}")
print(f"Latitude : {event['latitude']}")
print(f"Longitude: {event['longitude']}")


# --------------------------------------------------
# 2. NASA IMERG file
# --------------------------------------------------

rainfall_file = (
    "data/rainfall/"
    "3B-DAY.MS.MRG.3IMERG.20130712-S000000-E235959.V07B.nc4"
)

ds = xr.open_dataset(rainfall_file)

# --------------------------------------------------
# 3. Find nearest NASA grid cell
# --------------------------------------------------

rainfall = ds["precipitation"]

nearest = rainfall.sel(
    lat=event["latitude"],
    lon=event["longitude"],
    method="nearest"
)

print("\nNASA IMERG grid:")
print(f"Nearest latitude : {float(nearest.lat.values)}")
print(f"Nearest longitude: {float(nearest.lon.values)}")

print("\nRainfall:")
print(f"{float(nearest.values.squeeze()):.3f} mm/day")

ds.close()

print("\nTest completed successfully.")