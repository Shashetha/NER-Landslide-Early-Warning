import os
import time
import requests

OUTPUT_DIR = "data/soil_moisture/cci_daily"

BASE_URL = (
    "https://dap.ceda.ac.uk/neodc/esacci/"
    "soil_moisture/data/daily_files/"
    "COMBINED/v09.2"
)

FAILED_DATES = [
    "20100615",
    "20100904",
    "20100910",
    "20100912",
    "20100913",
    "20100916",
    "20101003",
    "20101009",
    "20110729",
    "20110805",
    "20140627",
    "20140628",
    "20140714",
    "20140814",
    "20140817",
    "20140908",
    "20140921",
    "20140922",
    "20140923",
    "20140924",
    "20141001",
    "20141005",
    "20150613",
    "20160728",
    "20160805",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

successful = 0
still_failed = []

for date_string in FAILED_DATES:

    year = date_string[:4]

    filename = (
        "ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-"
        f"{date_string}000000-fv09.2.nc"
    )

    url = f"{BASE_URL}/{year}/{filename}"
    output_path = os.path.join(OUTPUT_DIR, filename)
    temp_path = output_path + ".part"

    print(f"\n{date_string}")

    # Skip if already successfully downloaded
    if os.path.exists(output_path):
        print("    Already exists")
        continue

    success = False

    # Try each failed date up to 3 times
    for attempt in range(1, 4):

        print(f"    Attempt {attempt}/3")

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

                with open(temp_path, "wb") as f:

                    for chunk in response.iter_content(
                        chunk_size=256 * 1024
                    ):
                        if chunk:
                            f.write(chunk)

            size = os.path.getsize(temp_path)

            # CCI files are much larger than this
            if size < 100000:
                print(
                    f"    Invalid file size: {size} bytes"
                )

                os.remove(temp_path)
                continue

            os.replace(
                temp_path,
                output_path
            )

            print(
                f"    SUCCESS "
                f"({size / 1024:.1f} KB)"
            )

            successful += 1
            success = True
            break

        except Exception as e:

            print(f"    Failed: {e}")

            if os.path.exists(temp_path):
                os.remove(temp_path)

            time.sleep(5)

    if not success:
        still_failed.append(date_string)

    # Give the server a small break
    time.sleep(3)


print()
print("=" * 60)
print("RETRY COMPLETE")
print("=" * 60)

print(f"Recovered:    {successful}")
print(f"Still failed: {len(still_failed)}")

if still_failed:

    print("\nStill missing:")

    for date_string in still_failed:
        print(date_string)

else:

    print("\n✓ ALL 221 SOIL-MOISTURE DATES ARE AVAILABLE")