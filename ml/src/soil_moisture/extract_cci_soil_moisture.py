import os
import glob
import numpy as np
import pandas as pd
import xarray as xr


EVENT_FILE = "data/processed/ner_landslides_cleaned.csv"
INPUT_DIR = "data/soil_moisture/cci_daily"
OUTPUT_FILE = "data/processed/ner_soil_moisture_features.csv"


def find_variable(ds):
    """Find the soil-moisture variable in the NetCDF file."""

    candidates = [
        "sm",
        "soil_moisture",
        "soil_moisture_clim",
    ]

    for name in candidates:
        if name in ds.data_vars:
            return name

    # Fallback: use the first data variable
    variables = list(ds.data_vars)

    if not variables:
        raise ValueError("No data variable found in NetCDF file.")

    return variables[0]


def find_coordinate(ds, possible_names):
    """Find latitude/longitude coordinate name."""

    for name in possible_names:
        if name in ds.coords:
            return name

    for name in possible_names:
        if name in ds.variables:
            return name

    raise ValueError(
        f"Could not find coordinate. Tried: {possible_names}"
    )


# --------------------------------------------------
# Load landslide events
# --------------------------------------------------

events = pd.read_csv(EVENT_FILE)

events["event_date"] = pd.to_datetime(
    events["event_date"]
).dt.strftime("%Y%m%d")

print("Events:", len(events))


# --------------------------------------------------
# Build file lookup by date
# --------------------------------------------------

files = glob.glob(
    os.path.join(INPUT_DIR, "*.nc")
)

file_lookup = {}

for path in files:

    filename = os.path.basename(path)

    # Extract YYYYMMDD from filename
    parts = filename.split("-")

    date_string = None

    for part in parts:
        if len(part) >= 8 and part[:8].isdigit():
            date_string = part[:8]
            break

    if date_string:
        file_lookup[date_string] = path


print("Soil-moisture files found:", len(file_lookup))


# --------------------------------------------------
# Extract soil moisture
# --------------------------------------------------

results = []

failed = []

for index, event in events.iterrows():

    date_string = event["event_date"]

    print(
        f"[{index + 1}/{len(events)}] "
        f"{date_string} | "
        f"{event['latitude']:.4f}, "
        f"{event['longitude']:.4f}"
    )

    file_path = file_lookup.get(date_string)

    if file_path is None:

        print("    File not found")
        failed.append(event["event_id"])
        continue

    try:

        with xr.open_dataset(
            file_path,
            decode_times=True
        ) as ds:

            variable = find_variable(ds)

            lat_name = find_coordinate(
                ds,
                ["lat", "latitude"]
            )

            lon_name = find_coordinate(
                ds,
                ["lon", "longitude"]
            )

            lat = float(event["latitude"])
            lon = float(event["longitude"])

            # Nearest grid cell
            value = ds[variable].sel(
                {
                    lat_name: lat,
                    lon_name: lon
                },
                method="nearest"
            ).values

            value = np.asarray(value).squeeze()

            if np.size(value) == 1:
                value = float(value)
            else:
                value = float(
                    np.nanmean(value)
                )

            if not np.isfinite(value):
                value = np.nan

            results.append(
                {
                    "event_id": event["event_id"],
                    "event_date": event["event_date"],
                    "state": event["state"],
                    "latitude": event["latitude"],
                    "longitude": event["longitude"],
                    "soil_moisture": value
                }
            )

    except Exception as e:

        print("    ERROR:", e)
        failed.append(event["event_id"])


# --------------------------------------------------
# Save results
# --------------------------------------------------

result_df = pd.DataFrame(results)

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("=" * 60)
print("SOIL MOISTURE EXTRACTION COMPLETE")
print("=" * 60)

print("Successful:", len(result_df))
print("Failed:", len(failed))

if len(result_df) > 0:

    print()
    print(
        "Missing soil moisture:",
        result_df["soil_moisture"].isna().sum()
    )

    print()
    print(
        result_df["soil_moisture"].describe()
    )

print()
print("Saved to:")
print(OUTPUT_FILE)

if failed:

    print()
    print("Failed event IDs:")

    for event_id in failed:
        print(event_id)