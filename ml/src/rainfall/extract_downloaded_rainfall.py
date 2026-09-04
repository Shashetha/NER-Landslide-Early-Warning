import os
import re
import pandas as pd
import xarray as xr

RAINFALL_DIR = "data/rainfall"

LANDSLIDE_FILE = "data/processed/ner_landslides_cleaned.csv"
BACKGROUND_FILE = "data/processed/ner_background_samples.csv"

OUTPUT_FILE = "data/processed/ner_ml_dataset.csv"


# ============================================================
# 1. INDEX DOWNLOADED IMERG FILES
# ============================================================

print("=" * 60)
print("BUILDING NER ML DATASET")
print("=" * 60)

file_index = {}

for name in os.listdir(RAINFALL_DIR):

    if not name.endswith(".nc4"):
        continue

    if ".SUB.nc4" in name:
        continue

    match = re.search(r"(\d{8})", name)

    if match:
        file_index[match.group(1)] = os.path.join(
            RAINFALL_DIR,
            name
        )

print(f"\nIMERG files available: {len(file_index)}")


# ============================================================
# 2. RAINFALL CACHE
# ============================================================

rainfall_cache = {}


def get_rainfall(date, lat, lon):

    date_str = date.strftime("%Y%m%d")

    if date_str not in file_index:
        return None

    cache_key = (
        date_str,
        round(float(lat), 4),
        round(float(lon), 4)
    )

    if cache_key in rainfall_cache:
        return rainfall_cache[cache_key]

    try:

        ds = xr.open_dataset(file_index[date_str])

        value = ds["precipitation"].sel(
            lat=lat,
            lon=lon,
            method="nearest"
        ).values.squeeze()

        ds.close()

        if pd.isna(value):
            rainfall_cache[cache_key] = None
            return None

        value = float(value)

        rainfall_cache[cache_key] = value

        return value

    except Exception as error:

        print(
            f"ERROR reading {date_str}: {error}"
        )

        return None


# ============================================================
# 3. FUNCTION TO EXTRACT RAINFALL FEATURES
# ============================================================

def extract_features(date, lat, lon):

    rainfall_1d = get_rainfall(
        date,
        lat,
        lon
    )

    rainfall_3d_values = []

    for days_back in range(3):

        target_date = (
            date -
            pd.Timedelta(days=days_back)
        )

        value = get_rainfall(
            target_date,
            lat,
            lon
        )

        if value is not None:
            rainfall_3d_values.append(value)

    rainfall_3d = (
        sum(rainfall_3d_values)
        if len(rainfall_3d_values) == 3
        else None
    )


    rainfall_7d_values = []

    for days_back in range(7):

        target_date = (
            date -
            pd.Timedelta(days=days_back)
        )

        value = get_rainfall(
            target_date,
            lat,
            lon
        )

        if value is not None:
            rainfall_7d_values.append(value)

    rainfall_7d = (
        sum(rainfall_7d_values)
        if len(rainfall_7d_values) == 7
        else None
    )


    return (
        rainfall_1d,
        rainfall_3d,
        rainfall_7d
    )


# ============================================================
# 4. LOAD POSITIVE + BACKGROUND DATA
# ============================================================

landslides = pd.read_csv(
    LANDSLIDE_FILE
)

background = pd.read_csv(
    BACKGROUND_FILE
)


landslides["event_date"] = pd.to_datetime(
    landslides["event_date"],
    errors="coerce"
)

background["sample_date"] = pd.to_datetime(
    background["sample_date"],
    errors="coerce"
)


# ============================================================
# 5. STANDARDIZE COLUMNS
# ============================================================

positive = landslides[
    [
        "event_id",
        "event_date",
        "state",
        "latitude",
        "longitude"
    ]
].copy()

positive["target"] = 1


positive.rename(
    columns={
        "event_id": "sample_id"
    },
    inplace=True
)


negative = background[
    [
        "sample_id",
        "sample_date",
        "state",
        "latitude",
        "longitude",
        "target"
    ]
].copy()

negative.rename(
    columns={
        "sample_date": "event_date"
    },
    inplace=True
)


# ============================================================
# 6. COMBINE
# ============================================================

samples = pd.concat(
    [
        positive,
        negative
    ],
    ignore_index=True
)


print(
    f"\nPositive samples : "
    f"{(samples['target'] == 1).sum()}"
)

print(
    f"Background samples: "
    f"{(samples['target'] == 0).sum()}"
)

print(
    f"Total samples    : "
    f"{len(samples)}"
)


# ============================================================
# 7. EXTRACT RAINFALL
# ============================================================

results = []

print("\n" + "=" * 60)
print("EXTRACTING RAINFALL FEATURES")
print("=" * 60)

for index, row in samples.iterrows():

    date = row["event_date"]
    lat = row["latitude"]
    lon = row["longitude"]

    print(
        f"[{index + 1}/{len(samples)}] "
        f"{row['sample_id']} | "
        f"{date.date()} | "
        f"{row['state']} | "
        f"target={row['target']}"
    )

    rainfall_1d, rainfall_3d, rainfall_7d = (
        extract_features(
            date,
            lat,
            lon
        )
    )

    results.append({

        "sample_id":
            row["sample_id"],

        "event_date":
            date,

        "state":
            row["state"],

        "latitude":
            lat,

        "longitude":
            lon,

        "rainfall_1d":
            rainfall_1d,

        "rainfall_3d":
            rainfall_3d,

        "rainfall_7d":
            rainfall_7d,

        "target":
            row["target"]
    })


# ============================================================
# 8. SAVE ML DATASET
# ============================================================

ml_df = pd.DataFrame(results)

ml_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 9. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("NER ML DATASET CREATED")
print("=" * 60)

print(f"\nTotal samples: {len(ml_df)}")

print("\nTarget distribution:")

print(
    ml_df["target"]
    .value_counts()
    .sort_index()
)

print("\nRainfall availability:")

print(
    "1-day:",
    ml_df["rainfall_1d"].notna().sum()
)

print(
    "3-day:",
    ml_df["rainfall_3d"].notna().sum()
)

print(
    "7-day:",
    ml_df["rainfall_7d"].notna().sum()
)

print("\nSaved to:")

print(OUTPUT_FILE)
