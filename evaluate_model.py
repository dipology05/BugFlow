
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
)

# Load dataset
df = pd.read_csv("bugs_dataset.csv")

# Clean data
df = df.dropna(subset=["Short Description", "Severity Label"]).copy()
df["Short Description"] = df["Short Description"].astype(str).str.strip()
df["Severity Label"] = df["Severity Label"].str.strip().str.lower()
df = df[df["Short Description"] != ""]

# Convert original severity labels
severity_mapping = {
    "blocker": "Critical",
    "critical": "Critical",
    "major": "High",
    "normal": "Medium",
    "minor": "Low",
    "trivial": "Low",
}

df["target"] = df["Severity Label"].map(severity_mapping)
df = df.dropna(subset=["target"])

X = df["Short Description"]
y = df["target"]

# Create test dataset
_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# Load trained model
model = joblib.load("severity_model.joblib")

# Predict severity
predictions = model.predict(X_test)

labels = ["Critical", "High", "Low", "Medium"]

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n========== MODEL EVALUATION ==========")
print(f"Test samples: {len(y_test)}")
print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

# Precision, Recall, F1-score
print("\n========== CLASSIFICATION REPORT ==========")
print(
    classification_report(
        y_test,
        predictions,
        labels=labels,
        zero_division=0,
    )
)

# Confusion matrix
print("\n========== CONFUSION MATRIX ==========")
print("Rows = actual; columns = predicted")
print("Class order:", labels)
print(confusion_matrix(y_test, predictions, labels=labels))

# Sample predictions
print("\n========== SAMPLE PREDICTIONS ==========")

samples = [
    "Application crashes when user logs in",
    "Typo in error message",
    "SQL query fails when saving user data",
    "Critical security vulnerability allows unauthorized access",
]

for text in samples:
    prediction = model.predict([text])[0]
    print(f"\nBug: {text}")
    print(f"Predicted severity: {prediction}")

print("\n========== EVALUATION COMPLETE ==========")

