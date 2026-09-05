import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# --------------------------------------------------
# Load final dataset
# --------------------------------------------------

DATA_FILE = "data/processed/final_ml_dataset.csv"
MODEL_FILE = "ml/models/final_landslide_risk_model.joblib"

df = pd.read_csv(DATA_FILE)

print("Dataset loaded")
print("Total samples:", len(df))


# --------------------------------------------------
# Features and target
# --------------------------------------------------

features = [
    "rainfall_1d",
    "rainfall_3d",
    "rainfall_7d",
    "elevation_m",
    "slope_degrees",
    "soil_moisture"
]

X = df[features]
y = df["target"]


print()
print("Features:")
for feature in features:
    print("-", feature)

print()
print("Target distribution:")
print(y.value_counts().sort_index())


# --------------------------------------------------
# Train / test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print()
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# ML pipeline
# --------------------------------------------------

model = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    ),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
    )
])


# --------------------------------------------------
# Train
# --------------------------------------------------

print()
print("Training final Random Forest model...")

model.fit(X_train, y_train)

print("✓ Training completed")


# --------------------------------------------------
# Predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print()
print("=" * 60)
print("FINAL MODEL RESULTS")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-score : {f1:.4f}")

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print()
print("Classification Report:")
print(classification_report(y_test, y_pred))


# --------------------------------------------------
# Feature importance
# --------------------------------------------------

classifier = model.named_steps["classifier"]

importance = pd.DataFrame({
    "feature": features,
    "importance": classifier.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print()
print("Feature Importance:")
print(importance.to_string(index=False))


# --------------------------------------------------
# Save model
# --------------------------------------------------

joblib.dump(model, MODEL_FILE)

print()
print("✓ FINAL MODEL SAVED")
print(MODEL_FILE)