import streamlit as st
import joblib
import json
import os

# === CONFIG ===
SAVE_FOLDER = "D:/CostEstApp/Model"

# === Map label to Sr No ===
model_map = {
    "340-A": 340,
    "641-B": 641,
    "1017-C": 1017
}

# === Dropdown values for categorical features ===
categorical_options = {
    "Cushioning": ["CC", "CH","NC"],
    "Mounting": ["TM+RE","SPL","CM+RM","CM+RE","CC+RE"],
    "BearingY-N": ["Y", "N"],
    "ValveY-N": ["Y","N"],
    "Cyl Type": ["Arm","Boom","Bucket","Dipper","Lift","Stabilizer","Steering","Swing","Tilt","Other"]
}

# === Numerical input configurations ===
numerical_config = {
    "Pressure": {"min": 150, "max": 500, "step": 10, "default": 250},
    "Bore": {"min": 50, "max": 500, "step": 1, "default": 100},
    "Rod diameter": {"min": 50, "max": 500, "step": 1, "default": 75},
    "Stroke": {"min": 100, "max": 5000, "step": 1, "default": 750},
    "Tube_ID": {"min": 50, "max": 500, "step": 1, "default": 100},
    "Tube_OD": {"min": 50, "max": 500, "step": 1, "default": 120},
    "Rod_Length": {"min": 100, "max": 5000, "step": 10, "default": 900},
    "CEC_Thickness": {"min": 50, "max": 500, "step": 5, "default": 100},
    "Piston_Thickness": {"min": 50, "max": 500, "step": 5, "default": 100},
}

# === Streamlit App ===
st.title("🧠 Hydraulic Cylinder Cost Predictor")

# === Step 1: Model selection ===
model_label = st.selectbox("Select model", list(model_map.keys()))
sr_no = model_map[model_label]

# === Load model, features, encoders ===
model_path = f"{SAVE_FOLDER}/model_sr{sr_no}.pkl"
features_path = f"{SAVE_FOLDER}/model_sr{sr_no}_features.json"
encoders_path = f"{SAVE_FOLDER}/model_sr{sr_no}_encoders.pkl"

model = joblib.load(model_path)

with open(features_path, "r") as f:
    selected_features = json.load(f)

try:
    encoders = joblib.load(encoders_path)
except:
    encoders = {}

st.subheader(f"Enter inputs for Model {model_label}")

# === Step 2: Generate input fields ===
user_input = []
for feature in selected_features:
    if feature in categorical_options:
        val = st.selectbox(f"{feature}:", categorical_options[feature])
    elif feature in numerical_config:
        cfg = numerical_config[feature]
        val = st.slider(f"{feature}:", min_value=cfg["min"], max_value=cfg["max"], 
                        step=cfg["step"], value=cfg["default"])
    else:
        val = st.number_input(f"{feature}:", value=0.0)
    user_input.append(val)

# === Step 3: Predict ===
if st.button("Predict Overall Cost"):
    input_array = []
    for feature, val in zip(selected_features, user_input):
        if feature in encoders:
            val = encoders[feature].transform([val])[0]
        input_array.append(val)

    prediction = model.predict([input_array])[0]
    st.success(f"Predicted Overall Cost: ₹{prediction:,.2f}")
