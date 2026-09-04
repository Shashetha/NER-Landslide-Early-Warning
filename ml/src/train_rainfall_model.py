import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
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


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "data/processed/ner_ml_dataset.csv"
MODEL_DIR = "ml/models"
MODEL_FILE = os.path.join(MODEL_DIR, "rainfall_random_forest.joblib")

FEATURES = [
    "rainfall_1d",
    "rainfall_3d",
    "rainfall_7d"
]

TARGET = "target"


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("=" * 60)
print("NER LANDSLIDE RISK - RANDOM FOREST MODEL")
print("=" * 60)

print("\nLoading ML dataset...")

df = pd.read_csv(DATA_FILE)

print(f"Dataset loaded: {len(df)} samples")


# ============================================================
# 2. SELECT FEATURES AND TARGET
# ============================================================

X = df[FEATURES].copy()
y = df[TARGET].copy()

print("\nFeatures:")
for feature in FEATURES:
    print(f"  - {feature}")

print("\nTarget distribution:")
print(y.value_counts().sort_index())


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("HANDLING MISSING RAINFALL VALUES")
print("=" * 60)

print("\nMissing values before imputation:")

print(X.isna().sum())

imputer = SimpleImputer(strategy="median")

X_imputed = pd.DataFrame(
    imputer.fit_transform(X),
    columns=FEATURES,
    index=X.index
)

print("\nMissing values after imputation:")

print(X_imputed.isna().sum())


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 60)
print("TRAIN / TEST SPLIT")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X_imputed,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")


# ============================================================
# 5. TRAIN RANDOM FOREST
# ============================================================

print("\n" + "=" * 60)
print("TRAINING RANDOM FOREST")
print("=" * 60)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)

print("\nRandom Forest training completed.")


# ============================================================
# 6. PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# 7. MODEL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-score : {f1:.4f}")


# ============================================================
# 8. CONFUSION MATRIX
# ============================================================

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n                 Predicted")
print("              0          1")
print(f"Actual 0   {cm[0][0]:8d}   {cm[0][1]:8d}")
print(f"Actual 1   {cm[1][0]:8d}   {cm[1][1]:8d}")


# ============================================================
# 9. CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Background",
            "Landslide"
        ],
        zero_division=0
    )
)


# ============================================================
# 10. FEATURE IMPORTANCE
# ============================================================

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\n")

for _, row in importance.iterrows():

    print(
        f"{row['feature']:15s} : "
        f"{row['importance']:.4f}"
    )


# ============================================================
# 11. SAVE MODEL + IMPUTER
# ============================================================

print("\n" + "=" * 60)
print("SAVING MODEL")
print("=" * 60)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

model_package = {
    "model": model,
    "imputer": imputer,
    "features": FEATURES
}

joblib.dump(
    model_package,
    MODEL_FILE
)

print(f"\nModel saved to:")
print(MODEL_FILE)


# ============================================================
# 12. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("BASELINE ML TRAINING COMPLETE")
print("=" * 60)

print(f"\nSamples used      : {len(df)}")
print(f"Training samples  : {len(X_train)}")
print(f"Testing samples   : {len(X_test)}")

print(f"\nAccuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1-score  : {f1:.4f}")

print("\nModel:")
print(MODEL_FILE)

print("\nNEXT STEP:")
print("Review the real evaluation results before adding more features.")