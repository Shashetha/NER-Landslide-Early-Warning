import pandas as pd

INPUT_FILE = "data/processed/ner_rainfall_dataset.csv"
OUTPUT_FILE = "data/processed/missing_rainfall_dates.csv"

df = pd.read_csv(INPUT_FILE)

df["event_date"] = pd.to_datetime(df["event_date"])

missing_dates = set()

for _, row in df.iterrows():

    event_date = row["event_date"].normalize()

    # If 1-day rainfall is missing
    if pd.isna(row["rainfall_1d"]):
        missing_dates.add(event_date)

    # If 3-day rainfall is missing,
    # we need event day + previous 2 days
    if pd.isna(row["rainfall_3d"]):
        for days_back in range(3):
            missing_dates.add(
                event_date - pd.Timedelta(days=days_back)
            )

    # If 7-day rainfall is missing,
    # we need event day + previous 6 days
    if pd.isna(row["rainfall_7d"]):
        for days_back in range(7):
            missing_dates.add(
                event_date - pd.Timedelta(days=days_back)
            )

missing_dates = sorted(missing_dates)

result = pd.DataFrame({
    "date": missing_dates
})

result["date"] = result["date"].dt.strftime("%Y-%m-%d")

result.to_csv(OUTPUT_FILE, index=False)

print("=" * 60)
print("MISSING RAINFALL DATE LIST")
print("=" * 60)

print(f"\nUnique dates required: {len(result)}")

print("\nFirst 20 dates:")
print(result.head(20).to_string(index=False))

print("\nLast 20 dates:")
print(result.tail(20).to_string(index=False))

print(f"\nSaved to: {OUTPUT_FILE}")