import os
import pandas as pd
import xarray as xr
import numpy as np


# --------------------------------------------------
# Paths
# --------------------------------------------------

BACKGROUND_FILE = "data/processed/ner_background_samples.csv"
SOIL_MOISTURE_DIR = "data/soil_moisture/cci_daily"
OUTPUT_FILE = "data/processed/ner_background_soil_moisture_features.csv"


# --------------------------------------------------
# Load background samples
# --------------------------------------------------

df = pd.read_csv(BACKGROUND_FILE)

print("Background samples:", len(df))

results = []

successful = 0
failed = 0


# --------------------------------------------------
# Group samples by date
# --------------------------------------------------

grouped = df.groupby("sample_date")

print("Unique background dates:", len(grouped))
print()


# --------------------------------------------------
# Process one NetCDF file per date
# --------------------------------------------------

for sample_date, group in grouped:

    date_string = pd.to_datetime(sample_date).strftime("%Y%m%d")

    filename = (
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-"
        f"{date_string}000000-fv09.2.nc"
    )

    file_path = os.path.join(
        SOIL_MOISTURE_DIR,
        filename
    )

    print(
        f"Processing {date_string} "
        f"({len(group)} samples)..."
    )

    try:

        if not os.path.exists(file_path):

            print("    File missing")

            for _, row in group.iterrows():

                results.append({
                    "sample_id": row["sample_id"],
                    "sample_date": row["sample_date"],
                    "state": row["state"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "soil_moisture": np.nan,
                    "target": row["target"]
                })

            failed += len(group)
            continue


        # Open the NetCDF file ONCE
        with xr.open_dataset(
            file_path,
            engine="netcdf4"
        ) as ds:

            for _, row in group.iterrows():

                latitude = float(row["latitude"])
                longitude = float(row["longitude"])

                value = ds["sm"].sel(
                    lat=latitude,
                    lon=longitude,
                    method="nearest"
                ).values

                soil_moisture = float(
                    np.asarray(value).squeeze()
                )

                # Convert invalid values to NaN
                if not np.isfinite(soil_moisture):
                    soil_moisture = np.nan

                results.append({
                    "sample_id": row["sample_id"],
                    "sample_date": row["sample_date"],
                    "state": row["state"],
                    "latitude": latitude,
                    "longitude": longitude,
                    "soil_moisture": soil_moisture,
                    "target": row["target"]
                })

                successful += 1


    except Exception as e:

        print(f"    ERROR: {e}")

        for _, row in group.iterrows():

            results.append({
                "sample_id": row["sample_id"],
                "sample_date": row["sample_date"],
                "state": row["state"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "soil_moisture": np.nan,
                "target": row["target"]
            })

        failed += len(group)


# --------------------------------------------------
# Save results
# --------------------------------------------------

result_df = pd.DataFrame(results)

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("=" * 60)
print("BACKGROUND SOIL-MOISTURE EXTRACTION COMPLETE")
print("=" * 60)

print(f"Background samples: {len(df)}")
print(f"Successful:         {successful}")
print(f"Failed:             {failed}")

print()
print(
    "Missing soil moisture:",
    result_df["soil_moisture"].isna().sum()
)

print()
print("Soil moisture statistics:")

print(
    result_df["soil_moisture"].describe()
)

print()
print("Saved to:")
print(OUTPUT_FILE)