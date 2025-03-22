import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("car_data.csv")

# Convert 'Brand' & 'Fuel_Type' to numeric values
brand_encoder = LabelEncoder()
df["Brand"] = brand_encoder.fit_transform(df["Brand"])

fuel_encoder = LabelEncoder()
df["Fuel_Type"] = fuel_encoder.fit_transform(df["Fuel_Type"])

# Selecting features and target
X = df[["Brand", "Car_Age", "Driven_Kilometers", "Num_Owners", "Condition_Score", "Buying_Price", "Fuel_Type"]]
y = df["Resale_Price"]

# Splitting dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the trained model, scaler, and encoders
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

with open("brand_encoder.pkl", "wb") as brand_file:
    pickle.dump(brand_encoder, brand_file)

with open("fuel_encoder.pkl", "wb") as fuel_file:
    pickle.dump(fuel_encoder, fuel_file)

print("✅ Model, Scaler, and Encoders saved successfully!")
