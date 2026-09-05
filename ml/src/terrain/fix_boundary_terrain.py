import os
import math

import numpy as np
import pandas as pd
import rasterio
from rasterio.merge import merge


# ============================================================
# PATHS
# ============================================================

DEM_DIR = "data/terrain/dem"

INPUT_TERRAIN = "data/processed/ner_terrain_features.csv"
OUTPUT_TERRAIN = "data/processed/ner_terrain_features.csv"


# ============================================================
# EVENTS TO FIX
# ============================================================

TARGET_EVENTS = [714, 2411]


# ============================================================
# DEM TILE PATH
# ============================================================

def get_dem_path(lat, lon):

    lat_floor = math.floor(lat)
    lon_floor = math.floor(lon)

    lat_prefix = "N" if lat_floor >= 0 else "S"
    lon_prefix = "E" if lon_floor >= 0 else "W"

    lat_abs = abs(lat_floor)
    lon_abs = abs(lon_floor)

    tile_name = (
        f"Copernicus_DSM_COG_30_"
        f"{lat_prefix}{lat_abs:02d}_00_"
        f"{lon_prefix}{lon_abs:03d}_00_DEM.tif"
    )

    return os.path.join(DEM_DIR, tile_name)


# ============================================================
# SLOPE CALCULATION
# ============================================================

def calculate_slope(z, pixel_width_m, pixel_height_m):

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

    slope_radians = math.atan(
        math.sqrt(dz_dx ** 2 + dz_dy ** 2)
    )

    return math.degrees(slope_radians)


# ============================================================
# METRES PER DEGREE
# ============================================================

def degrees_to_meters(latitude):

    lat_rad = math.radians(latitude)

    meters_lat = (
        111132.92
        - 559.82 * math.cos(2 * lat_rad)
        + 1.175 * math.cos(4 * lat_rad)
        - 0.0023 * math.cos(6 * lat_rad)
    )

    meters_lon = (
        111412.84 * math.cos(lat_rad)
        - 93.5 * math.cos(3 * lat_rad)
        + 0.118 * math.cos(5 * lat_rad)
    )

    return meters_lat, meters_lon


# ============================================================
# EXTRACT FROM MOSAIC
# ============================================================

def extract_from_mosaic(paths, latitude, longitude):

    datasets = [
        rasterio.open(path)
        for path in paths
    ]

    try:

        mosaic, transform = merge(datasets)

        data = mosaic[0]

        # ----------------------------------------------------
        # Convert coordinate to mosaic row/column
        # ----------------------------------------------------

        col, row = ~transform * (longitude, latitude)

        col = int(math.floor(col))
        row = int(math.floor(row))

        # ----------------------------------------------------
        # Need complete 3x3 neighbourhood
        # ----------------------------------------------------

        if (
            row < 1
            or row >= data.shape[0] - 1
            or col < 1
            or col >= data.shape[1] - 1
        ):
            raise ValueError(
                f"3x3 neighbourhood unavailable: "
                f"row={row}, col={col}, "
                f"shape={data.shape}"
            )

        z = data[
            row - 1:row + 2,
            col - 1:col + 2
        ].astype(float)

        # ----------------------------------------------------
        # Check valid pixels
        # ----------------------------------------------------

        if np.any(~np.isfinite(z)):
            raise ValueError(
                "3x3 neighbourhood contains invalid values"
            )

        elevation = float(z[1, 1])

        # ----------------------------------------------------
        # Pixel dimensions
        # ----------------------------------------------------

        pixel_width_deg = abs(transform.a)
        pixel_height_deg = abs(transform.e)

        meters_lat, meters_lon = degrees_to_meters(latitude)

        pixel_width_m = pixel_width_deg * meters_lon
        pixel_height_m = pixel_height_deg * meters_lat

        slope = calculate_slope(
            z,
            pixel_width_m,
            pixel_height_m
        )

        return elevation, slope

    finally:

        for dataset in datasets:
            dataset.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("FIXING BOUNDARY TERRAIN EVENTS")
    print("=" * 60)

    df = pd.read_csv(INPUT_TERRAIN)

    # --------------------------------------------------------
    # Event 714
    # --------------------------------------------------------

    event_id = 714

    row_index = df.index[df["event_id"] == event_id]

    if len(row_index) == 0:
        raise ValueError("Event 714 not found")

    idx = row_index[0]

    lat = float(df.loc[idx, "latitude"])
    lon = float(df.loc[idx, "longitude"])

    print()
    print("Event 714")
    print(f"Coordinate: {lat}, {lon}")

    paths = [
        get_dem_path(27, 93),
        get_dem_path(27, 94)
    ]

    print("Using neighboring tiles:")
    for path in paths:
        print(f"  {os.path.basename(path)}")

    elevation, slope = extract_from_mosaic(
        paths,
        lat,
        lon
    )

    df.loc[idx, "elevation_m"] = elevation
    df.loc[idx, "slope_degrees"] = slope
    df.loc[idx, "dem_tile"] = (
        "N27/E093 + N27/E094 boundary"
    )

    print(f"Elevation: {elevation:.2f} m")
    print(f"Slope:     {slope:.2f}°")

    # --------------------------------------------------------
    # Event 2411
    # --------------------------------------------------------

    event_id = 2411

    row_index = df.index[df["event_id"] == event_id]

    if len(row_index) == 0:
        raise ValueError("Event 2411 not found")

    idx = row_index[0]

    lat = float(df.loc[idx, "latitude"])
    lon = float(df.loc[idx, "longitude"])

    print()
    print("Event 2411")
    print(f"Coordinate: {lat}, {lon}")

    paths = [
        get_dem_path(26, 93),
        get_dem_path(27, 93)
    ]

    print("Using neighboring tiles:")
    for path in paths:
        print(f"  {os.path.basename(path)}")

    elevation, slope = extract_from_mosaic(
        paths,
        lat,
        lon
    )

    df.loc[idx, "elevation_m"] = elevation
    df.loc[idx, "slope_degrees"] = slope
    df.loc[idx, "dem_tile"] = (
        "N26/E093 + N27/E093 boundary"
    )

    print(f"Elevation: {elevation:.2f} m")
    print(f"Slope:     {slope:.2f}°")

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_TERRAIN,
        index=False
    )

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("BOUNDARY FIX COMPLETE")
    print("=" * 60)

    check = df[
        df["event_id"].isin(TARGET_EVENTS)
    ][
        [
            "event_id",
            "latitude",
            "longitude",
            "elevation_m",
            "slope_degrees"
        ]
    ]

    print(check.to_string(index=False))

    print()
    print(
        "Missing elevation:",
        df["elevation_m"].isna().sum()
    )

    print(
        "Missing slope:",
        df["slope_degrees"].isna().sum()
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()