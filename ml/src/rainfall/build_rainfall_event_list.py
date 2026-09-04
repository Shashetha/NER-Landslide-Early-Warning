import pandas as pd

# Load cleaned NER landslide data
input_file = "data/processed/ner_landslides_cleaned.csv"

df = pd.read_csv(input_file)

# Make sure event_date is a proper date
df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

# Keep only the information needed for rainfall extraction
rainfall_events = df[
    [
        "event_id",
        "event_date",
        "state",
        "latitude",
        "longitude"
    ]
].copy()

# Add rainfall window dates
rainfall_events["rainfall_1d_date"] = rainfall_events["event_date"]

rainfall_events["rainfall_3d_start"] = (
    rainfall_events["event_date"] - pd.Timedelta(days=2)
)

rainfall_events["rainfall_7d_start"] = (
    rainfall_events["event_date"] - pd.Timedelta(days=6)
)

# Sort by date
rainfall_events = rainfall_events.sort_values("event_date")

# Save list
output_file = "data/processed/rainfall_event_list.csv"

rainfall_events.to_csv(output_file, index=False)

print("=" * 60)
print("RAINFALL EVENT LIST CREATED")
print("=" * 60)

print(f"\nTotal landslide events: {len(rainfall_events)}")

print("\nDate range:")
print(rainfall_events["event_date"].min())
print("to")
print(rainfall_events["event_date"].max())

print("\nFirst 10 events:")
print(rainfall_events.head(10).to_string(index=False))

print(f"\nSaved to: {output_file}")