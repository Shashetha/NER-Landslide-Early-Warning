import os
import pandas as pd
import earthaccess


# ============================================================
# CONFIGURATION
# ============================================================

DATE_FILE = "data/processed/missing_rainfall_dates.csv"
RAINFALL_DIR = "data/rainfall"

os.makedirs(RAINFALL_DIR, exist_ok=True)


# ============================================================
# 1. LOAD REQUIRED DATES
# ============================================================

print("=" * 60)
print("NASA IMERG MISSING DATE DOWNLOADER")
print("=" * 60)

dates_df = pd.read_csv(DATE_FILE)

dates_df["date"] = pd.to_datetime(
    dates_df["date"],
    errors="coerce"
)

dates_df = dates_df.dropna(subset=["date"])

required_dates = sorted(
    dates_df["date"].dt.strftime("%Y-%m-%d").unique()
)

print(f"\nRequired dates: {len(required_dates)}")


# ============================================================
# 2. NASA EARTHDATA LOGIN
# ============================================================

print("\nLogging into NASA Earthdata...")

earthaccess.login()

print("NASA Earthdata authentication successful!")


# ============================================================
# 3. DOWNLOAD EACH REQUIRED DATE
# ============================================================

downloaded_count = 0
already_exists = 0
failed_count = 0

for index, date_string in enumerate(required_dates, start=1):

    date_obj = pd.Timestamp(date_string)

    date_compact = date_obj.strftime("%Y%m%d")

    expected_filename = (
        f"3B-DAY.MS.MRG.3IMERG."
        f"{date_compact}-S000000-E235959.V07B.nc4"
    )

    local_path = os.path.join(
        RAINFALL_DIR,
        expected_filename
    )

    print(
        f"\n[{index}/{len(required_dates)}] "
        f"{date_string}"
    )

    # --------------------------------------------------------
    # Skip existing file
    # --------------------------------------------------------

    if os.path.exists(local_path):

        print("Already exists — skipping.")

        already_exists += 1

        continue

    # --------------------------------------------------------
    # Search NASA
    # --------------------------------------------------------

    print("Searching NASA Earthdata...")

    try:

        results = earthaccess.search_data(
            short_name="GPM_3IMERGDF",
            version="07",
            temporal=(date_string, date_string)
        )

    except Exception as error:

        print(f"Search failed: {error}")

        failed_count += 1

        continue

    if not results:

        print("No NASA file found.")

        failed_count += 1

        continue

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    print("Downloading IMERG file...")

    try:

        files = earthaccess.download(
            results[0],
            RAINFALL_DIR
        )

        if files:

            print("Download successful.")

            downloaded_count += 1

        else:

            print("Download returned no file.")

            failed_count += 1

    except Exception as error:

        print(f"Download failed: {error}")

        failed_count += 1


# ============================================================
# 4. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DOWNLOAD SUMMARY")
print("=" * 60)

print(f"\nRequired dates : {len(required_dates)}")
print(f"Downloaded     : {downloaded_count}")
print(f"Already existed: {already_exists}")
print(f"Failed         : {failed_count}")

print(f"\nRainfall folder:")
print(RAINFALL_DIR)

print("\nYou can safely rerun this script.")
print("Existing files will be skipped.")