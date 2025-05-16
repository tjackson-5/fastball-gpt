
# streamlit_app.py

import streamlit as st
from fastball_lite import generate_pnl_forecast, apply_experience_curve, apply_half_life
from math import log, exp

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

# --- Learning Half-Life Forecaster ---
st.header("Learning Half-Life Forecaster")

metric_label = st.text_input("Metric to Model (e.g., Lead Time, OEE)", "Lead Time")
d0 = st.number_input("Current Value", value=20.0)
dmin = st.number_input("Ideal Minimum", value=8.0)
cycles = st.slider("Number of Improvement Cycles", 1, 12, 4)
maturity = st.selectbox("Hoshin Kanri Maturity Level (Likert 1–5)", [1, 2, 3, 4, 5])

# Half-life mapping (cycles to halve ignorance)
half_life_lookup = {1: 6, 2: 4, 3: 3, 4: 2, 5: 1}
hl = half_life_lookup[maturity]

if st.button("Forecast Learning"):
    projected = dmin + (d0 - dmin) * exp(-log(2) * cycles / hl)
    st.success(f"Projected {metric_label} after {cycles} cycles: {projected:.2f}")
    st.caption(f"Assumes {100 * (1 - 2**(-1 / hl)):.1f}% ignorance reduction per cycle at maturity level {maturity}.")
