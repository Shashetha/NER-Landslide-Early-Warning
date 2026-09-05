import os
import pandas as pd
import numpy as np
import rasterio
from rasterio.warp import transform


# --------------------------------------------------
# Paths
# --------------------------------------------------

BACKGROUND_FILE = "data/processed/ner_background_samples.csv"
DEM_DIR = "data/terrain/dem"
OUTPUT_FILE = "data/processed/ner_background_terrain_features.csv"


# --------------------------------------------------
# Load background samples
# --------------------------------------------------

df = pd.read_csv(BACKGROUND_FILE)

print("Background samples:", len(df))


# --------------------------------------------------
# Find DEM tile
# --------------------------------------------------

def find_dem_tile(latitude, longitude):

    lat_degree = int(np.floor(latitude))
    lon_degree = int(np.floor(longitude))

    lat_part = f"N{lat_degree:02d}_00"
    lon_part = f"E{lon_degree:03d}_00"

    prefix = (
        f"Copernicus_DSM_COG_30_"
        f"{lat_part}_{lon_part}_DEM"
    )

    matches = [
        os.path.join(DEM_DIR, f)
        for f in os.listdir(DEM_DIR)
        if f.startswith(prefix)
        and f.endswith(".tif")
    ]

    if not matches:
        return None

    return matches[0]


# --------------------------------------------------
# Extract terrain
# --------------------------------------------------

results = []

successful = 0
failed = 0


for index, sample in df.iterrows():

    sample_id = sample["sample_id"]

    latitude = float(sample["latitude"])
    longitude = float(sample["longitude"])

    print(
        f"[{index + 1}/{len(df)}] "
        f"{sample_id}"
    )

    try:

        dem_file = find_dem_tile(
            latitude,
            longitude
        )

        if dem_file is None:
            raise FileNotFoundError(
                "DEM tile not found"
            )

        with rasterio.open(dem_file) as src:

            row_index, col_index = src.index(
                longitude,
                latitude
            )

            # Check coordinate is inside tile
            if (
                row_index < 0
                or row_index >= src.height
                or col_index < 0
                or col_index >= src.width
            ):
                raise ValueError(
                    "Coordinate outside DEM tile"
                )

            # --------------------------------------
            # Elevation
            # --------------------------------------

            elevation = float(
                src.read(
                    1,
                    window=rasterio.windows.Window(
                        col_index,
                        row_index,
                        1,
                        1
                    )
                )[0, 0]
            )

            # --------------------------------------
            # 3 x 3 elevation window
            # --------------------------------------

            r0 = max(0, row_index - 1)
            c0 = max(0, col_index - 1)

            r1 = min(src.height, row_index + 2)
            c1 = min(src.width, col_index + 2)

            window = rasterio.windows.Window(
                c0,
                r0,
                c1 - c0,
                r1 - r0
            )

            elevation_window = src.read(
                1,
                window=window
            ).astype(float)

            # --------------------------------------
            # Correct slope calculation
            # --------------------------------------
            # DEM is geographic (degrees).
            # Convert pixel spacing from degrees
            # to approximate metres at this latitude.

            pixel_width_deg = abs(
                src.transform.a
            )

            pixel_height_deg = abs(
                src.transform.e
            )

            meters_per_degree_lat = 111320.0

            meters_per_degree_lon = (
                111320.0 *
                np.cos(
                    np.radians(latitude)
                )
            )

            x_resolution = (
                pixel_width_deg *
                meters_per_degree_lon
            )

            y_resolution = (
                pixel_height_deg *
                meters_per_degree_lat
            )

            if (
                elevation_window.shape[0] < 2
                or elevation_window.shape[1] < 2
            ):

                slope = np.nan

            else:

                dz_dy, dz_dx = np.gradient(
                    elevation_window,
                    y_resolution,
                    x_resolution
                )

                gradient = np.sqrt(
                    dz_dx ** 2 +
                    dz_dy ** 2
                )

                slope_array = np.degrees(
                    np.arctan(gradient)
                )

                center_row = row_index - r0
                center_col = col_index - c0

                center_row = min(
                    max(center_row, 0),
                    slope_array.shape[0] - 1
                )

                center_col = min(
                    max(center_col, 0),
                    slope_array.shape[1] - 1
                )

                slope = float(
                    slope_array[
                        center_row,
                        center_col
                    ]
                )

        results.append({
            "sample_id": sample_id,
            "sample_date": sample["sample_date"],
            "state": sample["state"],
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation,
            "slope": slope,
            "target": sample["target"]
        })

        successful += 1

    except Exception as e:

        print(
            f"    FAILED: {e}"
        )

        results.append({
            "sample_id": sample_id,
            "sample_date": sample["sample_date"],
            "state": sample["state"],
            "latitude": latitude,
            "longitude": longitude,
            "elevation": np.nan,
            "slope": np.nan,
            "target": sample["target"]
        })

        failed += 1


# --------------------------------------------------
# Save
# --------------------------------------------------

result_df = pd.DataFrame(results)

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Validation summary
# --------------------------------------------------

print()
print("=" * 60)
print("BACKGROUND TERRAIN EXTRACTION COMPLETE")
print("=" * 60)

print(f"Background samples: {len(df)}")
print(f"Successful:         {successful}")
print(f"Failed:             {failed}")

print()
print(
    "Missing elevation:",
    result_df["elevation"].isna().sum()
)

print(
    "Missing slope:",
    result_df["slope"].isna().sum()
)

print()
print("Elevation statistics:")
print(result_df["elevation"].describe())

print()
print("Slope statistics:")
print(result_df["slope"].describe())

print()
print("Saved to:")
print(OUTPUT_FILE)