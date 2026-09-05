import os
import time
import requests
import pandas as pd


EVENT_FILE = "data/processed/ner_background_samples.csv"
OUTPUT_DIR = "data/soil_moisture/cci_daily"

BASE_URL = (
    "https://dap.ceda.ac.uk/neodc/esacci/"
    "soil_moisture/data/daily_files/"
    "COMBINED/v09.2"
)


# --------------------------------------------------
# Load background samples
# --------------------------------------------------

df = pd.read_csv(EVENT_FILE)

df["sample_date"] = pd.to_datetime(
    df["sample_date"]
).dt.strftime("%Y%m%d")

required_dates = sorted(
    df["sample_date"].unique()
)

print("Background samples:", len(df))
print("Unique background dates:", len(required_dates))


os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------
# Download only missing dates
# --------------------------------------------------

downloaded = 0
already_exists = 0
failed_dates = []


for date_string in required_dates:

    year = date_string[:4]

    filename = (
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-"
        f"{date_string}000000-fv09.2.nc"
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    temp_path = output_path + ".part"

    print(f"\n{date_string}")

    # Already downloaded
    if os.path.exists(output_path):

        print("    Already exists")
        already_exists += 1
        continue


    url = f"{BASE_URL}/{year}/{filename}"

    success = False


    # --------------------------------------------------
    # Retry up to 3 times
    # --------------------------------------------------

    for attempt in range(1, 4):

        print(
            f"    Attempt {attempt}/3"
        )

        try:

            with requests.get(
                url,
                stream=True,
                timeout=(30, 180)
            ) as response:

                if response.status_code != 200:

                    print(
                        f"    HTTP {response.status_code}"
                    )

                    continue


                with open(
                    temp_path,
                    "wb"
                ) as f:

                    for chunk in response.iter_content(
                        chunk_size=256 * 1024
                    ):

                        if chunk:
                            f.write(chunk)


            size = os.path.getsize(
                temp_path
            )


            # Basic file-size validation
            if size < 100000:

                print(
                    f"    Invalid file size: "
                    f"{size} bytes"
                )

                os.remove(temp_path)
                continue


            # Move completed download into place
            os.replace(
                temp_path,
                output_path
            )


            print(
                f"    SUCCESS "
                f"({size / 1024:.1f} KB)"
            )

            downloaded += 1
            success = True

            break


        except Exception as e:

            print(
                f"    Failed: {e}"
            )

            if os.path.exists(temp_path):

                os.remove(temp_path)

            time.sleep(5)


    if not success:

        failed_dates.append(
            date_string
        )


    # Small delay between dates
    time.sleep(2)


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print()
print("=" * 60)
print("BACKGROUND SOIL-MOISTURE DOWNLOAD COMPLETE")
print("=" * 60)

print(
    f"Downloaded:       {downloaded}"
)

print(
    f"Already existed:  {already_exists}"
)

print(
    f"Failed:           {len(failed_dates)}"
)


if failed_dates:

    print()
    print("Failed dates:")

    for date_string in failed_dates:

        print(date_string)

else:

    print()
    print(
        "✓ ALL BACKGROUND DATES ARE AVAILABLE"
    )