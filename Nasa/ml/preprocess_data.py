# FarmShift AI
# Module 6 - Data Preprocessing

import pandas as pd

from sklearn.model_selection import train_test_split


# Load dataset

df = pd.read_csv("ml/dataset/Crop_recommendation.csv")


# Separate input features

X = df.drop("label", axis=1)


# Separate output labels

y = df["label"]


# Split dataset into training and testing data

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y

)


# Display dataset information

print("\nDATA PREPROCESSING COMPLETED!")

print("\nTotal Records:", len(df))

print("Training Records:", len(X_train))

print("Testing Records:", len(X_test))

print("\nInput Features:")
print(X.columns.tolist())

print("\nOutput Categories:")
print(y.nunique())

print("\nTraining and Testing Data Ready!")