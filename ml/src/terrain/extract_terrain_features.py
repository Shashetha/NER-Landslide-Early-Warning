import os
import math
import glob

import numpy as np
import pandas as pd
import rasterio


# ============================================================
# PATHS
# ============================================================

INPUT_CSV = "data/processed/ner_landslides_cleaned.csv"
DEM_DIR = "data/terrain/dem"
OUTPUT_CSV = "data/processed/ner_terrain_features.csv"


# ============================================================
# FUNCTIONS
# ============================================================

def get_dem_tile(latitude, longitude):
    """
    Determine the 1-degree DEM tile containing a coordinate.
    """

    lat_floor = math.floor(latitude)
    lon_floor = math.floor(longitude)

    lat_prefix = "N" if lat_floor >= 0 else "S"
    lon_prefix = "E" if lon_floor >= 0 else "W"

    lat_abs = abs(lat_floor)
    lon_abs = abs(lon_floor)

    tile_name = (
        f"Copernicus_DSM_COG_30_"
        f"{lat_prefix}{lat_abs:02d}_00_"
        f"{lon_prefix}{lon_abs:03d}_00_DEM.tif"
    )

    tile_path = os.path.join(DEM_DIR, tile_name)

    return tile_path


def degrees_to_meters(latitude):
    """
    Approximate metres represented by one degree of latitude
    and longitude at a given latitude.
    """

    lat_rad = math.radians(latitude)

    meters_per_degree_lat = (
        111132.92
        - 559.82 * math.cos(2 * lat_rad)
        + 1.175 * math.cos(4 * lat_rad)
        - 0.0023 * math.cos(6 * lat_rad)
    )

    meters_per_degree_lon = (
        111412.84 * math.cos(lat_rad)
        - 93.5 * math.cos(3 * lat_rad)
        + 0.118 * math.cos(5 * lat_rad)
    )

    return meters_per_degree_lat, meters_per_degree_lon


def extract_features(src, latitude, longitude):
    """
    Extract elevation and local slope from a DEM.

    Elevation:
        Nearest DEM pixel to the landslide coordinate.

    Slope:
        Horn's 3x3 method using neighbouring elevation pixels.
        Result is expressed in degrees.
    """

    # Convert geographic coordinate to raster row/column
    row, col = src.index(longitude, latitude)

    # --------------------------------------------------------
    # Read 3x3 neighbourhood
    # --------------------------------------------------------

    window = rasterio.windows.Window(
        col_off=col - 1,
        row_off=row - 1,
        width=3,
        height=3
    )

    data = src.read(1, window=window, masked=True)

    # Make sure a complete 3x3 neighbourhood was obtained
    if data.shape != (3, 3):
        return np.nan, np.nan

    # Check for missing / invalid pixels
    if np.ma.is_masked(data):
        if np.any(data.mask):
            return np.nan, np.nan

    z = np.asarray(data, dtype=float)

    if not np.all(np.isfinite(z)):
        return np.nan, np.nan

    # --------------------------------------------------------
    # Elevation
    # --------------------------------------------------------

    elevation = float(z[1, 1])

    # --------------------------------------------------------
    # Pixel dimensions
    # --------------------------------------------------------

    pixel_width_deg = abs(src.transform.a)
    pixel_height_deg = abs(src.transform.e)

    meters_lat, meters_lon = degrees_to_meters(latitude)

    pixel_width_m = pixel_width_deg * meters_lon
    pixel_height_m = pixel_height_deg * meters_lat

    # Prevent division by zero
    if pixel_width_m <= 0 or pixel_height_m <= 0:
        return elevation, np.nan

    # --------------------------------------------------------
    # Horn's slope calculation
    #
    # z1 z2 z3
    # z4 z5 z6
    # z7 z8 z9
    # --------------------------------------------------------

    dz_dx = (
        (z[0, 2] + 2 * z[1, 2] + z[2, 2])
        -
        (z[0, 0] + 2 * z[1, 0] + z[2, 0])
    ) / (8 * pixel_width_m)

    dz_dy = (
        (z[2, 0] + 2 * z[2, 1] + z[2, 2])
        -
        (z[0, 0] + 2 * z[0, 1] + z[0, 2])
    ) / (8 * pixel_height_m)

    # --------------------------------------------------------
    # Convert gradient to slope in degrees
    # --------------------------------------------------------

    slope_radians = math.atan(
        math.sqrt(dz_dx ** 2 + dz_dy ** 2)
    )

    slope_degrees = math.degrees(slope_radians)

    return elevation, slope_degrees


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("NER TERRAIN FEATURE EXTRACTION")
    print("=" * 60)

    # --------------------------------------------------------
    # Load landslide dataset
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_CSV)

    print(f"Historical landslide events: {len(df)}")
    print()

    # --------------------------------------------------------
    # Check required columns
    # --------------------------------------------------------

    required_columns = [
        "event_id",
        "event_date",
        "state",
        "latitude",
        "longitude"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------------------------
    # Find DEM files
    # --------------------------------------------------------

    dem_files = glob.glob(
        os.path.join(DEM_DIR, "*.tif")
    )

    print(f"DEM tiles available: {len(dem_files)}")
    print()

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    results = []

    failed = []

    # --------------------------------------------------------
    # Process every event
    # --------------------------------------------------------

    for index, event in df.iterrows():

        event_id = event["event_id"]
        latitude = float(event["latitude"])
        longitude = float(event["longitude"])

        dem_path = get_dem_tile(
            latitude,
            longitude
        )

        print(
            f"[{index + 1}/{len(df)}] "
            f"Event {event_id} "
            f"({latitude:.4f}, {longitude:.4f})"
        )

        # ----------------------------------------------------
        # Check DEM tile
        # ----------------------------------------------------

        if not os.path.exists(dem_path):

            print("    DEM tile NOT FOUND")

            failed.append({
                "event_id": event_id,
                "reason": "DEM tile not found"
            })

            results.append({
                "event_id": event_id,
                "event_date": event["event_date"],
                "state": event["state"],
                "latitude": latitude,
                "longitude": longitude,
                "elevation_m": np.nan,
                "slope_degrees": np.nan,
                "dem_tile": os.path.basename(dem_path)
            })

            continue

        try:

            with rasterio.open(dem_path) as src:

                elevation, slope = extract_features(
                    src,
                    latitude,
                    longitude
                )

                results.append({
                    "event_id": event_id,
                    "event_date": event["event_date"],
                    "state": event["state"],
                    "latitude": latitude,
                    "longitude": longitude,
                    "elevation_m": elevation,
                    "slope_degrees": slope,
                    "dem_tile": os.path.basename(dem_path)
                })

                if np.isnan(elevation) or np.isnan(slope):

                    print(
                        "    Could not calculate terrain features"
                    )

                    failed.append({
                        "event_id": event_id,
                        "reason": "Invalid DEM neighbourhood"
                    })

                else:

                    print(
                        f"    Elevation: {elevation:.2f} m"
                    )

                    print(
                        f"    Slope:     {slope:.2f} degrees"
                    )

        except Exception as e:

            print(f"    ERROR: {e}")

            failed.append({
                "event_id": event_id,
                "reason": str(e)
            })

            results.append({
                "event_id": event_id,
                "event_date": event["event_date"],
                "state": event["state"],
                "latitude": latitude,
                "longitude": longitude,
                "elevation_m": np.nan,
                "slope_degrees": np.nan,
                "dem_tile": os.path.basename(dem_path)
            })

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT_CSV,
        index=False
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    valid_elevation = result_df["elevation_m"].notna().sum()
    valid_slope = result_df["slope_degrees"].notna().sum()

    print()
    print("=" * 60)
    print("TERRAIN EXTRACTION COMPLETE")
    print("=" * 60)

    print(f"Total events:       {len(result_df)}")
    print(f"Valid elevation:    {valid_elevation}")
    print(f"Valid slope:        {valid_slope}")
    print(f"Failed events:      {len(failed)}")

    print()

    if valid_elevation > 0:

        print("Elevation statistics:")
        print(
            f"  Minimum: {result_df['elevation_m'].min():.2f} m"
        )
        print(
            f"  Maximum: {result_df['elevation_m'].max():.2f} m"
        )
        print(
            f"  Mean:    {result_df['elevation_m'].mean():.2f} m"
        )

    print()

    if valid_slope > 0:

        print("Slope statistics:")
        print(
            f"  Minimum: {result_df['slope_degrees'].min():.2f}°"
        )
        print(
            f"  Maximum: {result_df['slope_degrees'].max():.2f}°"
        )
        print(
            f"  Mean:    {result_df['slope_degrees'].mean():.2f}°"
        )

    print()
    print(f"Saved to: {OUTPUT_CSV}")

    # --------------------------------------------------------
    # Failed events
    # --------------------------------------------------------

    if failed:

        print()
        print("Failed events:")

        for item in failed[:20]:
            print(
                f"  Event {item['event_id']}: "
                f"{item['reason']}"
            )

        if len(failed) > 20:
            print(
                f"  ... and {len(failed) - 20} more"
            )

    else:

        print()
        print("✓ ALL EVENTS HAVE VALID TERRAIN FEATURES")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()