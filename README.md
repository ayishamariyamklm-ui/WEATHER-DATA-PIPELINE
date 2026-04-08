#  Weather Data Pipeline 

An end-to-end **Data Engineering Project** that collects, processes, monitors, and visualizes real-time weather data using a modular ETL pipeline with alerts, monitoring, and dashboards.

---

##  Features

-  Automated ETL Pipeline (Extract, Transform, Load)
-  Real-time Weather API Integration
-  Data Validation & Cleaning
-  Alert System (Temperature & Humidity thresholds)
-  Interactive Dashboard (Streamlit)
-  SQLite Database Storage
-  Logging System (Pipeline, Errors, Alerts)
-  Health Check System
-  Automated Backup System
-  Report Generation
-  Unit Testing (Pytest)

---

##  Project Structure


weather-data-pipeline-advanced
│
├── README.md
├── requirements.txt
│
├── config
│   ├──__init__.py
│   └── config.py
│
├── src
│   ├──__init__.py
│   ├── api_client.py
│   ├── database.py
│   ├── etl_pipeline.py
│   ├── scheduler.py
│   ├── validators.py
│   ├── reporter.py
│   ├── monitor.py
│   └── alerts.py
│
├── dashboard
│   └── dashboard.py
│
├── database/
│   ├── __init__.py         
│   ├── weather_data.db 
│   ├──  init_db.py 
│   └──  schema.sql 
│
├── logs/
│    ├── pipeline.log            
│    ├── error.log               
│    └──  alerts.log                
│
│
├── reports
│   └── weather_report.txt
│
├── tests/
│    ├── test_api.py
│    ├── test_database.py
│    ├── test_pipeline.py
│    ├── test_validators.py
│    └── __init__.py 
│                                                                                                   │                                             
├── scripts/
│    ├── setup_database.py
│    ├── run_pipeline.py
│    ├── generate_report.py
│    ├── backup_database.py
│    ├── health_check.py
│
└── docs
    ├── architecture.md
    ├── dashboard_guide.md
    └── troubleshooting.md


---

##  Tech Stack

- Python 3.10+
- Pandas
- Requests
- SQLite
- Streamlit
- Pytest
- Logging

---

##  Dashboard Features

- Weather data table
- Temperature trends
- Humidity trends
- Alerts visualization

---

## Use Cases

- Weather Monitoring Systems
- Smart City Dashboards
- IoT Data Pipelines
- Real-time Analytics Systems

---

## Future Improvements

- Deploy on AWS / Render
- Add Machine Learning predictions
- Email/SMS alert system
- Docker containerization


# 👩‍💻 Author
## AYISHA MARIYAM
### Aspiring Data Scientist
