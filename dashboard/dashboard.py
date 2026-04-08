import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import sqlite3

from config.config import DB_PATH


# ================================
# PAGE CONFIG
# ================================

st.set_page_config(
    page_title="Weather Monitoring Dashboard",
    layout="wide"
)

st.title("Weather Data Monitoring Dashboard")


# ================================
# LOAD DATA
# ================================

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    weather_df = pd.read_sql("SELECT * FROM weather_data", conn)
    alerts_df = pd.read_sql("SELECT * FROM alerts", conn)

    conn.close()

    # Fix timestamp parsing issue
    if not weather_df.empty:
        weather_df["timestamp"] = pd.to_datetime(
            weather_df["timestamp"], format="ISO8601"
        )

    if not alerts_df.empty:
        alerts_df["timestamp"] = pd.to_datetime(
            alerts_df["timestamp"], format="ISO8601"
        )

    return weather_df, alerts_df


weather_df, alerts_df = load_data()


# ================================
# SIDEBAR FILTERS
# ================================

st.sidebar.header("Filters")

cities = weather_df["city"].unique() if not weather_df.empty else []
selected_city = st.sidebar.selectbox("Select City", cities)


# ================================
# FILTER DATA
# ================================

if selected_city:
    filtered_weather = weather_df[weather_df["city"] == selected_city]
    filtered_alerts = alerts_df[alerts_df["city"] == selected_city]
else:
    filtered_weather = weather_df
    filtered_alerts = alerts_df


# ================================
# KPI METRICS
# ================================

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(filtered_weather))

if not filtered_weather.empty:
    col2.metric("Avg Temperature", f"{filtered_weather['temperature'].mean():.2f} C")
    col3.metric("Avg Humidity", f"{filtered_weather['humidity'].mean():.2f}%")
else:
    col2.metric("Avg Temperature", "N/A")
    col3.metric("Avg Humidity", "N/A")

col4.metric("Total Alerts", len(filtered_alerts))


# ================================
# TEMPERATURE TREND
# ================================

st.subheader("Temperature Trend")

if not filtered_weather.empty:
    temp_chart = filtered_weather.set_index("timestamp")["temperature"]
    st.line_chart(temp_chart)
else:
    st.warning("No temperature data available")


# ================================
# HUMIDITY TREND
# ================================

st.subheader("Humidity Trend")

if not filtered_weather.empty:
    humidity_chart = filtered_weather.set_index("timestamp")["humidity"]
    st.line_chart(humidity_chart)
else:
    st.warning("No humidity data available")


# ================================
# ALERTS TABLE
# ================================

st.subheader("Recent Alerts")

if not filtered_alerts.empty:
    st.dataframe(filtered_alerts.sort_values(by="timestamp", ascending=False))
else:
    st.info("No alerts available")


# ================================
# RAW DATA VIEW
# ================================

st.subheader("Raw Weather Data")

if not filtered_weather.empty:
    st.dataframe(filtered_weather.sort_values(by="timestamp", ascending=False))
else:
    st.info("No weather data available")
