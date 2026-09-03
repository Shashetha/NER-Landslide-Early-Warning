import pandas as pd

# Load NASA landslide dataset
df = pd.read_csv("data/raw/rows.csv")

# NER states
ner_states = [
    "Assam",
    "Arunachal Pradesh",
    "Arunāchal Pradesh",
    "Manipur",
    "Meghalaya",
    "Meghālaya",
    "Mizoram",
    "Nagaland",
    "Nāgāland",
    "Sikkim",
    "Tripura"
]

# Filter NER records
ner = df[df["admin_division_name"].isin(ner_states)].copy()

# Normalize state names
state_mapping = {
    "Arunāchal Pradesh": "Arunachal Pradesh",
    "Nāgāland": "Nagaland",
    "Meghālaya": "Meghalaya"
}

ner["state"] = ner["admin_division_name"].replace(state_mapping)

# Select useful columns
cleaned = ner[
    [
        "event_id",
        "event_date",
        "event_title",
        "landslide_trigger",
        "landslide_size",
        "landslide_setting",
        "country_name",
        "state",
        "latitude",
        "longitude",
        "fatality_count",
        "injury_count"
    ]
].copy()

# Convert date
cleaned["event_date"] = pd.to_datetime(
    cleaned["event_date"],
    errors="coerce"
)

# Sort by date
cleaned = cleaned.sort_values("event_date")

# Save processed dataset
cleaned.to_csv(
    "data/processed/ner_landslides_cleaned.csv",
    index=False
)

print("=" * 60)
print("NER DATA PREPARATION COMPLETE")
print("=" * 60)

print(f"\nTotal records: {len(cleaned)}")

print("\nColumns:")
print(cleaned.columns.tolist())

print("\nEvents by state:")
print(cleaned["state"].value_counts())

print("\nDate range:")
print(cleaned["event_date"].min())
print("to")
print(cleaned["event_date"].max())

print("\nMissing values:")
print(cleaned.isnull().sum())

print("\nSaved to:")
print("data/processed/ner_landslides_cleaned.csv")