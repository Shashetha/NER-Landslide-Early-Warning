import pandas as pd

# Load the original NASA dataset
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

ner["state_normalized"] = ner["admin_division_name"].replace(state_mapping)

print("=" * 60)
print("NER LANDSLIDE DATA INSPECTION")
print("=" * 60)

print(f"\nTotal NER events: {len(ner)}")

print("\nEvents by state:")
print(ner["state_normalized"].value_counts())

print("\nLandslide triggers:")
print(ner["landslide_trigger"].value_counts(dropna=False))

print("\nMissing values:")
print(ner.isnull().sum().sort_values(ascending=False))

print("\nCoordinate check:")
print(f"Missing latitude: {ner['latitude'].isna().sum()}")
print(f"Missing longitude: {ner['longitude'].isna().sum()}")

print("\nLatitude range:")
print(ner["latitude"].min(), "to", ner["latitude"].max())

print("\nLongitude range:")
print(ner["longitude"].min(), "to", ner["longitude"].max())

# Check duplicate coordinates
duplicate_coordinates = ner[
    ner.duplicated(["latitude", "longitude"], keep=False)
].sort_values(["latitude", "longitude"])

print("\nRecords with duplicate coordinates:")
print(len(duplicate_coordinates))

if len(duplicate_coordinates) > 0:
    print(
        duplicate_coordinates[
            [
                "event_date",
                "event_title",
                "admin_division_name",
                "latitude",
                "longitude",
            ]
        ].to_string(index=False)
    )

print("\nInspection complete.")