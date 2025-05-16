
# streamlit_app.py

import streamlit as st
from fastball_lite import generate_pnl_forecast, apply_experience_curve

st.title("Fastball Lite Dashboard")

# --- Value Stream P&L Forecast ---
st.header("5-Year Value Stream P&L Forecast")

units = st.number_input("Annual Unit Sales", value=10000)
price = st.number_input("Average Sales Price ($)", value=5000)
years = 5

material_cost = [st.number_input(f"Material Cost Year {i+1}", value=40000000 + i*4000000) for i in range(years)]
conversion_cost = [st.number_input(f"Conversion Cost Year {i+1}", value=8000000 - i*400000) for i in range(years)]
dev_cost = [st.number_input(f"Development Cost Year {i+1}", value=1400000) for i in range(years)]

if st.button("Run P&L Forecast"):
    pnl = generate_pnl_forecast(units, price, material_cost, conversion_cost, dev_cost, years)
    st.subheader("Forecast Results")
    st.dataframe(pnl)

# --- Experience Curve Forecaster ---
st.header("Experience Curve Forecaster")

initial_cost = st.number_input("Initial Unit Cost ($)", value=5000)
initial_ct = st.number_input("Current Lead Time (days)", value=20)
target_ct = st.number_input("Target Lead Time (days)", value=10)
learning_param = st.slider("Learning Parameter (e.g. 0.85 = 15% gain)", 0.6, 1.0, 0.85)

if st.button("Calculate Experience Curve Savings"):
    new_cost = apply_experience_curve(initial_cost, initial_ct, target_ct, learning_param)
    st.success(f"New Predicted Unit Cost: ${new_cost:,.2f}")
    st.caption("Based on experience curve dynamics relative to lead time reduction.")
