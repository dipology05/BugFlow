
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# 1. Load dataset
df = pd.read_csv("bugs_dataset.csv")

# 2. Clean text and labels
df = df.dropna(subset=["Short Description", "Severity Label"]).copy()
df["Short Description"] = df["Short Description"].astype(str).str.strip()
df["Severity Label"] = df["Severity Label"].str.strip().str.lower()

df = df[df["Short Description"] != ""]

# 3. Map original labels into four severity levels
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

# 4. Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 5. Build TF-IDF + Logistic Regression pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=30000,
            ngram_range=(1, 2),
        ),
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
        ),
    ),
])

# 6. Train model
print("Training model... Please wait.")
model.fit(X_train, y_train)

# 7. Evaluate on unseen test data
predictions = model.predict(X_test)

print("\n--- MODEL RESULTS ---")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Accuracy:", round(accuracy_score(y_test, predictions), 4))

print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_test, predictions, zero_division=0))

# 8. Save trained model
joblib.dump(model, "severity_model.joblib")

print("\nModel saved as severity_model.joblib")
