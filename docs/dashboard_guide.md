#  Dashboard Guide

## Overview

The dashboard is built using **Streamlit** and provides real-time insights into weather data.

---

##  How to Run

python -m streamlit run dashboard/dashboard.py

---

## Dashboard Features

### City-wise Weather Overview

- Temperature
- Humidity
- Wind Speed
- Timestamp

Displayed using tables and metrics.

### Trend Visualizations

- Temperature trends over time
- Humidity trends
- Multi-city comparison

Helps in identifying patterns and anomalies.

### Alerts Panel

Displays alerts triggered by:

- High Temperature
- Low Temperature
- High Humidity

Each alert includes:

- City
- Alert Type
- Value
- Timestamp

---

## Data Source

The dashboard reads data from:

- database/weather_data.db

Tables used:

- weather_data
- alerts

---

## Key Components in dashboard.py

### Load Data

- @st.cache_data
- def load_data():
- Caches data for performance
- Reduces DB queries

### Data Cleaning

- weather_df["timestamp"] = pd.to_datetime(weather_df["timestamp"], format="ISO8601")

Fixes timestamp parsing issues.

### Metrics Display

- st.metric("Temperature", value)

Used for quick insights.

### Charts

- st.line_chart()
- st.bar_chart()

---

## Best Practices

- Always run pipeline before dashboard
- Use caching for performance
- Keep UI simple and readable
- Avoid heavy computations in dashboard

---

## Future Improvements 

- Add filters (city, date range)
- Add download button (CSV export)
- Add real-time auto refresh
- Deploy using Streamlit Cloud / Docker

---

## Testing the Dashboard

- Run pipeline
- Insert sample data
- Launch dashboard
Verify:
- Charts load correctly
- Alerts appear
- Data updates

---

## Summary

The dashboard provides:

- Real-time insights
- Alert monitoring
- Trend analysis

It is the visual layer the data pipeline.