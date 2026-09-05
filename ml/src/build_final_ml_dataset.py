import pandas as pd


# --------------------------------------------------
# Input files
# --------------------------------------------------

rainfall_file = "data/processed/ner_ml_dataset.csv"

positive_terrain_file = (
    "data/processed/ner_terrain_features.csv"
)

background_terrain_file = (
    "data/processed/ner_background_terrain_features.csv"
)

positive_sm_file = (
    "data/processed/ner_soil_moisture_features.csv"
)

background_sm_file = (
    "data/processed/ner_background_soil_moisture_features.csv"
)

output_file = (
    "data/processed/final_ml_dataset.csv"
)


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

rainfall = pd.read_csv(rainfall_file)

positive_terrain = pd.read_csv(
    positive_terrain_file
)

background_terrain = pd.read_csv(
    background_terrain_file
)

positive_sm = pd.read_csv(
    positive_sm_file
)

background_sm = pd.read_csv(
    background_sm_file
)


print("Rainfall samples:", len(rainfall))
print(
    "Positive terrain samples:",
    len(positive_terrain)
)
print(
    "Background terrain samples:",
    len(background_terrain)
)
print(
    "Positive soil-moisture samples:",
    len(positive_sm)
)
print(
    "Background soil-moisture samples:",
    len(background_sm)
)


# --------------------------------------------------
# Normalize positive IDs
# --------------------------------------------------

positive_terrain = positive_terrain.rename(
    columns={"event_id": "sample_id"}
)

positive_sm = positive_sm.rename(
    columns={"event_id": "sample_id"}
)

# Convert all IDs to the same type
rainfall["sample_id"] = rainfall["sample_id"].astype(str)
positive_terrain["sample_id"] = positive_terrain["sample_id"].astype(str)
background_terrain["sample_id"] = background_terrain["sample_id"].astype(str)
positive_sm["sample_id"] = positive_sm["sample_id"].astype(str)
background_sm["sample_id"] = background_sm["sample_id"].astype(str)

# --------------------------------------------------
# Combine terrain
# --------------------------------------------------

terrain = pd.concat(
    [
        positive_terrain[
            [
                "sample_id",
                "elevation_m",
                "slope_degrees"
            ]
        ],
        background_terrain[
            [
                "sample_id",
                "elevation",
                "slope"
            ]
        ].rename(
            columns={
                "elevation": "elevation_m",
                "slope": "slope_degrees"
            }
        )
    ],
    ignore_index=True
)


# --------------------------------------------------
# Combine soil moisture
# --------------------------------------------------

soil_moisture = pd.concat(
    [
        positive_sm[
            [
                "sample_id",
                "soil_moisture"
            ]
        ],
        background_sm[
            [
                "sample_id",
                "soil_moisture"
            ]
        ]
    ],
    ignore_index=True
)


print()
print("Combined terrain samples:", len(terrain))
print(
    "Combined soil-moisture samples:",
    len(soil_moisture)
)


# --------------------------------------------------
# Select rainfall columns
# --------------------------------------------------

rainfall = rainfall[
    [
        "sample_id",
        "event_date",
        "state",
        "latitude",
        "longitude",
        "rainfall_1d",
        "rainfall_3d",
        "rainfall_7d",
        "target"
    ]
]


# --------------------------------------------------
# Merge rainfall + terrain
# --------------------------------------------------

final_df = rainfall.merge(
    terrain,
    on="sample_id",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# Merge soil moisture
# --------------------------------------------------

final_df = final_df.merge(
    soil_moisture,
    on="sample_id",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# Arrange final columns
# --------------------------------------------------

final_df = final_df[
    [
        "sample_id",
        "event_date",
        "state",
        "latitude",
        "longitude",
        "rainfall_1d",
        "rainfall_3d",
        "rainfall_7d",
        "elevation_m",
        "slope_degrees",
        "soil_moisture",
        "target"
    ]
]


# --------------------------------------------------
# Validation
# --------------------------------------------------

print()
print("=" * 60)
print("FINAL ML DATASET VALIDATION")
print("=" * 60)

print(
    "Total samples:",
    len(final_df)
)

print()
print("Target distribution:")
print(
    final_df["target"]
    .value_counts()
    .sort_index()
)

print()
print(
    "Unique sample IDs:",
    final_df["sample_id"].nunique()
)

print()
print(
    "Duplicate sample IDs:",
    final_df["sample_id"]
    .duplicated()
    .sum()
)

print()
print("Missing values:")
print(
    final_df.isna().sum()
)

print()
print("Feature statistics:")

print(
    final_df[
        [
            "rainfall_1d",
            "rainfall_3d",
            "rainfall_7d",
            "elevation_m",
            "slope_degrees",
            "soil_moisture"
        ]
    ].describe()
)


# --------------------------------------------------
# Critical checks
# --------------------------------------------------

assert len(final_df) == 702

assert final_df["sample_id"].nunique() == 702

assert final_df["sample_id"].isna().sum() == 0

assert (
    final_df["target"]
    .value_counts()
    .sort_index()
    .to_dict()
    == {0: 351, 1: 351}
)

assert (
    final_df["elevation_m"].notna().sum()
    == 702
)

assert (
    final_df["slope_degrees"].notna().sum()
    == 702
)


# --------------------------------------------------
# Save
# --------------------------------------------------

final_df.to_csv(
    output_file,
    index=False
)


print()
print("✓ ALL BASIC VALIDATION CHECKS PASSED")

print()
print("Saved to:")
print(output_file)