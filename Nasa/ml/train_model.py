# FarmShift AI
# Module 6 - Random Forest Model Training


import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# Get current file location

BASE_DIR = Path(__file__).resolve().parent


# Load dataset

dataset_path = BASE_DIR / "dataset" / "Crop_recommendation.csv"

df = pd.read_csv(dataset_path)


# Separate input features

X = df.drop("label", axis=1)


# Separate output labels

y = df["label"]


# Split dataset

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y

)


# Create Random Forest model

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)


# Train the model

print("\nTraining Random Forest Model...")

model.fit(X_train, y_train)


# Make predictions

y_pred = model.predict(X_test)


# Calculate accuracy

accuracy = accuracy_score(y_test, y_pred)


print("\n========== MODEL EVALUATION ==========")

print("\nModel Accuracy:", accuracy * 100, "%")


# Classification report

print("\nClassification Report:")

print(classification_report(y_test, y_pred))


# Confusion matrix

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, y_pred))


# Save trained model

model_path = BASE_DIR / "crop_model.pkl"

joblib.dump(model, model_path)


print("\nModel saved successfully!")

print("Location:", model_path)


print("\nRANDOM FOREST TRAINING COMPLETED!")