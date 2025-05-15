
# streamlit_app.py

import streamlit as st
from fastball_lite import generate_pnl_forecast

st.title("Fastball Lite: Value Stream P&L Forecast")

units = st.number_input("Annual Unit Sales", value=10000)
price = st.number_input("Average Sales Price ($)", value=5000)
years = 5

material_cost = [st.number_input(f"Material Cost Year {i+1}", value=40000000 + i*4000000) for i in range(years)]
conversion_cost = [st.number_input(f"Conversion Cost Year {i+1}", value=8000000 - i*400000) for i in range(years)]
dev_cost = [st.number_input(f"Development Cost Year {i+1}", value=1400000) for i in range(years)]

if st.button("Run Forecast"):
    pnl = generate_pnl_forecast(units, price, material_cost, conversion_cost, dev_cost, years)
    st.subheader("5-Year Value Stream Forecast")
    st.dataframe(pnl)
