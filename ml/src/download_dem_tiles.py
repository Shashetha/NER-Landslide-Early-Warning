import os
import math
import pandas as pd
import boto3

from botocore import UNSIGNED
from botocore.config import Config


# -----------------------------------------
# Project paths
# -----------------------------------------

CSV_PATH = "data/processed/ner_landslides_cleaned.csv"
OUTPUT_DIR = "data/terrain/dem"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------------------
# AWS public S3 client
# -----------------------------------------

s3 = boto3.client(
    "s3",
    region_name="eu-central-1",
    config=Config(signature_version=UNSIGNED)
)

BUCKET = "copernicus-dem-90m"


# -----------------------------------------
# Read landslide coordinates
# -----------------------------------------

df = pd.read_csv(CSV_PATH)

tiles = sorted(
    set(
        (math.floor(row.latitude), math.floor(row.longitude))
        for row in df.itertuples()
    )
)

print(f"Events: {len(df)}")
print(f"Unique DEM tiles needed: {len(tiles)}")
print()


# -----------------------------------------
# Download required DEM tiles
# -----------------------------------------

success = 0
failed = 0

for lat, lon in tiles:

    lat_prefix = "N" if lat >= 0 else "S"
    lon_prefix = "E" if lon >= 0 else "W"

    lat_abs = abs(lat)
    lon_abs = abs(lon)

    tile_name = (
        f"Copernicus_DSM_COG_30_"
        f"{lat_prefix}{lat_abs:02d}_00_"
        f"{lon_prefix}{lon_abs:03d}_00_DEM"
    )

    key = f"{tile_name}/{tile_name}.tif"
    output_path = os.path.join(OUTPUT_DIR, f"{tile_name}.tif")

    print(f"[{success + failed + 1}/{len(tiles)}] {tile_name}")

    if os.path.exists(output_path):
        print("  Already exists — skipping.")
        success += 1
        continue

    try:

        s3.download_file(
            BUCKET,
            key,
            output_path
        )

        print("  Downloaded.")
        success += 1

    except Exception as e:

        print(f"  FAILED: {e}")
        failed += 1


# -----------------------------------------
# Final report
# -----------------------------------------

print()
print("=" * 50)
print("DEM DOWNLOAD COMPLETE")
print("=" * 50)
print(f"Successful: {success}")
print(f"Failed:     {failed}")
print(f"Total:      {len(tiles)}")
print(f"Folder:     {OUTPUT_DIR}")