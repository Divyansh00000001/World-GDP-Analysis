import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import pickle

# Load the dataset
df = pd.read_csv("U:\My Files\VS code\minor project\World-GDP-Analysis-and-Prediction-main\countries of the world.csv")

# Clean and preprocess
df = df.dropna(subset=["GDP ($ per capita)"])
def safe_to_float(val):
    if isinstance(val, str):
        return float(val.replace(",", "."))
    return float(val)

df["GDP ($ per capita)"] = df["GDP ($ per capita)"].apply(safe_to_float)
df["Literacy (%)"] = df["Literacy (%)"].apply(safe_to_float)
df["Agriculture"] = df["Agriculture"].apply(safe_to_float)
df["Birthrate"] = df["Birthrate"].apply(safe_to_float)




# Use only numeric columns for simplicity
X = df[["Literacy (%)", "Agriculture", "Birthrate"]]
X = X.fillna(X.mean())

y = df["GDP ($ per capita)"]

# Train the model
model = DecisionTreeRegressor()
model.fit(X, y)

# Save the model
with open("model_dtr.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model retrained and saved as model_dtr.pkl")
