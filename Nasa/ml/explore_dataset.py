# FarmShift AI
# Module 6 - Dataset Exploration

import pandas as pd

# Load the crop recommendation dataset

df = pd.read_csv("ml/dataset/Crop_recommendation.csv")


# Display dataset information

print("\n========== DATASET INFORMATION ==========")

print("\nFirst 5 records:")
print(df.head())


# Display number of rows and columns

print("\nDataset Shape:")
print(df.shape)


# Display column names

print("\nDataset Columns:")
print(df.columns.tolist())


# Check missing values

print("\nMissing Values:")
print(df.isnull().sum())


# Check duplicate records

print("\nDuplicate Records:")
print(df.duplicated().sum())


# Display crop categories

print("\nCrop Categories:")
print(df["label"].value_counts())


# Display statistical information

print("\nStatistical Information:")
print(df.describe())


print("\nDATASET EXPLORATION COMPLETED!")