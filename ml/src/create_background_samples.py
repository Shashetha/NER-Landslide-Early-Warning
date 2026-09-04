import os
import re
import pandas as pd
import numpy as np


INPUT_FILE = "data/processed/ner_landslides_cleaned.csv"
RAINFALL_DIR = "data/rainfall"
OUTPUT_FILE = "data/processed/ner_background_samples.csv"

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# LOAD LANDSLIDE EVENTS
# ============================================================

df = pd.read_csv(INPUT_FILE)

df["event_date"] = pd.to_datetime(
    df["event_date"],
    errors="coerce"
)

print("=" * 60)
print("CREATING IMERG-COVERED NER BACKGROUND SAMPLES")
print("=" * 60)

print(f"\nLandslide events: {len(df)}")


# ============================================================
# FIND EXISTING IMERG DATES
# ============================================================

rainfall_dates = set()

for filename in os.listdir(RAINFALL_DIR):

    if not filename.endswith(".nc4"):
        continue

    if ".SUB.nc4" in filename:
        continue

    match = re.search(r"(\d{8})", filename)

    if match:
        rainfall_dates.add(
            pd.to_datetime(
                match.group(1),
                format="%Y%m%d"
            ).strftime("%Y-%m-%d")
        )


print(
    f"Existing IMERG dates available: "
    f"{len(rainfall_dates)}"
)


# ============================================================
# KNOWN LANDSLIDE DATE + LOCATION PAIRS
# ============================================================

known_events = set(
    zip(
        df["event_date"].dt.strftime("%Y-%m-%d"),
        df["latitude"].round(4),
        df["longitude"].round(4)
    )
)


# ============================================================
# CREATE BACKGROUND SAMPLES
# ============================================================

background_samples = []

available_dates = sorted(rainfall_dates)

for _, event in df.iterrows():

    state = event["state"]
    latitude = float(event["latitude"])
    longitude = float(event["longitude"])

    candidates = []

    for date in available_dates:

        candidate = (
            date,
            round(latitude, 4),
            round(longitude, 4)
        )

        # Don't use the same date/location as a known landslide
        if candidate not in known_events:
            candidates.append(date)

    if not candidates:
        continue

    background_date = rng.choice(candidates)

    background_samples.append({
        "sample_id": f"BG_{event['event_id']}",
        "sample_date": background_date,
        "state": state,
        "latitude": latitude,
        "longitude": longitude,
        "target": 0
    })


# ============================================================
# SAVE
# ============================================================

background_df = pd.DataFrame(background_samples)

background_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("BACKGROUND SAMPLE CREATION COMPLETE")
print("=" * 60)

print(
    f"\nBackground samples created: "
    f"{len(background_df)}"
)

print("\nSamples per state:")

print(
    background_df
    .groupby("state")
    .size()
    .sort_values(ascending=False)
)

print("\nFirst 10 samples:")

print(
    background_df
    .head(10)
    .to_string(index=False)
)

print(f"\nSaved to: {OUTPUT_FILE}")