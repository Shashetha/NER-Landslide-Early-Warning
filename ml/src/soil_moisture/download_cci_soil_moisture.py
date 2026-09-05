import os
import re
import requests
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_CSV = "data/processed/ner_landslides_cleaned.csv"

OUTPUT_DIR = "data/soil_moisture/cci_daily"

BASE_URL = (
    "https://dap.ceda.ac.uk/neodc/esacci/"
    "soil_moisture/data/daily_files/"
    "COMBINED/v09.2"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD EVENT DATES
# ============================================================

df = pd.read_csv(INPUT_CSV)

df["event_date"] = pd.to_datetime(
    df["event_date"],
    errors="coerce"
)

if df["event_date"].isna().any():
    raise ValueError("Some event dates could not be parsed.")

dates = sorted(
    df["event_date"].dt.strftime("%Y%m%d").unique()
)

print("=" * 60)
print("ESA CCI SOIL MOISTURE TARGETED DOWNLOAD")
print("=" * 60)

print(f"Historical events: {len(df)}")
print(f"Unique dates required: {len(dates)}")
print()


# ============================================================
# DOWNLOAD
# ============================================================

session = requests.Session()

successful = 0
skipped = 0
failed = []

for i, date_string in enumerate(dates, 1):

    year = date_string[:4]

    filename = (
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-"
        f"{date_string}000000-fv09.2.nc"
    )

    url = f"{BASE_URL}/{year}/{filename}"

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    print(
        f"[{i}/{len(dates)}] "
        f"{date_string}"
    )

    # --------------------------------------------------------
    # Already downloaded?
    # --------------------------------------------------------

    if os.path.exists(output_path):

        size = os.path.getsize(output_path)

        if size > 0:

            print(
                f"    Already exists "
                f"({size / 1024:.1f} KB)"
            )

            skipped += 1
            continue

    temp_path = output_path + ".part"

    try:

        response = session.get(
            url,
            stream=True,
            timeout=60
        )

        if response.status_code != 200:

            print(
                f"    FAILED - HTTP "
                f"{response.status_code}"
            )

            failed.append(
                (date_string, response.status_code)
            )

            response.close()
            continue

        with open(temp_path, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    file.write(chunk)

        response.close()

        file_size = os.path.getsize(temp_path)

        if file_size == 0:

            print("    FAILED - empty file")

            os.remove(temp_path)

            failed.append(
                (date_string, "empty file")
            )

            continue

        # Only rename after successful download
        os.replace(
            temp_path,
            output_path
        )

        print(
            f"    Downloaded "
            f"({file_size / 1024:.1f} KB)"
        )

        successful += 1

    except Exception as e:

        print(f"    FAILED - {e}")

        failed.append(
            (date_string, str(e))
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 60)
print("SOIL MOISTURE DOWNLOAD COMPLETE")
print("=" * 60)

print(f"Unique dates required: {len(dates)}")
print(f"Downloaded:            {successful}")
print(f"Already existed:       {skipped}")
print(f"Failed:                {len(failed)}")

print()
print(f"Folder: {OUTPUT_DIR}")

if failed:

    print()
    print("Failed dates:")

    for date_string, reason in failed[:20]:

        print(
            f"  {date_string}: {reason}"
        )

    if len(failed) > 20:

        print(
            f"  ... and "
            f"{len(failed) - 20} more"
        )

else:

    print()
    print("✓ ALL REQUIRED SOIL-MOISTURE FILES AVAILABLE")