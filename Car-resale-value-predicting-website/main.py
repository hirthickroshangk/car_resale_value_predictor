from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import pickle
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load Model, Scaler, and Label Encoder
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

with open("label_encoder.pkl", "rb") as le_file:
    label_encoder = pickle.load(le_file)

# Load car data
df = pd.read_csv("car_data.csv")
brands = df["Brand"].unique().tolist()
fuel_types = df["Fuel_Type"].unique().tolist()  # Extract unique fuel types

# Ensure logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Helper functions for logging
def log_action(file, data):
    with open(f"logs/{file}", "a") as f:
        f.write(",".join(map(str, data)) + "\n")

def read_logs(file, columns):
    if os.path.exists(f"logs/{file}"):
        return pd.read_csv(f"logs/{file}", names=columns).to_dict(orient="records")
    return []

# Routes
@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]
        users = {"admin": "admin123", "customer": "customer123"}

        if username in users and users[username] == password:
            session["username"] = username
            log_action("login_history.csv", [username, datetime.now()])
            return redirect(url_for("predict")) if username == "customer" else redirect(url_for("admin_dashboard"))
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "username" not in session or session["username"] != "customer":
        return redirect(url_for("login"))

    predicted_price = None
    if request.method == "POST":
        brand = request.form["brand"]
        fuel_type = request.form["fuel_type"]
        
        brand_encoded = label_encoder.transform([brand])[0]  # Convert brand to number
        
        data = [
            brand_encoded,  
            float(request.form["age"]),
            float(request.form["kilometers"]),
            int(request.form["owners"]),
            float(request.form["condition"]),
            float(request.form["original_price"]),
            float(fuel_types.index(fuel_type)),  
        ]

        # Scale the input before prediction
        data_scaled = scaler.transform([data])
        predicted_price = model.predict(data_scaled)[0]

        # Ensure resale price is not higher than buying price
        buying_price = float(request.form["original_price"])
        if predicted_price > buying_price:
            predicted_price = buying_price * 0.85  # Adjust to 85% max of buying price

        # **Log the prediction history (THIS FIXES THE ISSUE)**
        log_action("prediction_history.csv", [
            session["username"], brand, request.form["age"], request.form["kilometers"],
            request.form["owners"], request.form["condition"], request.form["original_price"],
            predicted_price, fuel_type, datetime.now()
        ])

    return render_template("predict.html", brands=brands, fuel_types=fuel_types, predicted_price=predicted_price)


@app.route("/admin")
def admin_dashboard():
    if "username" not in session or session["username"] != "admin":
        return redirect(url_for("login"))

    login_history = read_logs("login_history.csv", ["Username", "Timestamp"])
    prediction_history = read_logs("prediction_history.csv", ["Username", "Brand", "Age", "Kilometers", "Owners", "Condition", "Original Price", "Predicted Price", "Fuel Type", "Timestamp"])

    return render_template("admin.html", login_history=login_history, prediction_history=prediction_history)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
