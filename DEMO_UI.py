
import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.title("🛰️ PM2.5 Spatial Estimator (Demo UI)")

# Sidebar Inputs
st.sidebar.header("🔧 Input Parameters")
area_name = st.sidebar.text_input("Urban Area Name", "Delhi")
latitude = st.sidebar.number_input("Latitude (center point)", value=28.61, format="%.4f")
longitude = st.sidebar.number_input("Longitude (center point)", value=77.23, format="%.4f")
time_of_day = st.sidebar.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
pm_type = st.sidebar.selectbox("PM Concentration Type", ["PM2.5", "PM10", "NO2", "SO2"])

st.sidebar.markdown("---")
generate = st.sidebar.button("Generate Spatial Map")

# Mock prediction data
def generate_mock_data(center_lat, center_lon):
    lats = np.linspace(center_lat - 0.05, center_lat + 0.05, 5)
    lons = np.linspace(center_lon - 0.05, center_lon + 0.05, 5)
    data = []
    for lat in lats:
        for lon in lons:
            value = np.random.uniform(50, 180)  # mock PM2.5 values
            data.append({"lat": lat, "lon": lon, "pm": round(value, 1)})
    return pd.DataFrame(data)

if generate:
    st.success(f"Generated mock {pm_type} spatial map for {area_name} ({time_of_day})")

    df = generate_mock_data(latitude, longitude)
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    for _, row in df.iterrows():
        color = "green" if row["pm"] < 60 else "orange" if row["pm"] < 100 else "red"
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            fill=True,
            color=color,
            fill_opacity=0.7,
            popup=f"{pm_type}: {row['pm']} µg/m³"
        ).add_to(m)

    st_folium(m, width=800, height=500)
else:
    st.info("Use the sidebar to input parameters and generate the spatial map.")
