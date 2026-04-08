from pathlib import Path
import os

# ================================
# PROJECT ROOT PATH
# ================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ================================
# DATABASE CONFIGURATION
# ================================

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "weather.db"
DB_PATH = DATABASE_DIR / "weather_data.db"

SCHEMA_PATH = DATABASE_DIR / "schema.sql"


# ================================
# API CONFIGURATION
# ================================

API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key_here")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

CITIES = [
    "Mumbai",
    "Delhi",
    "Chennai",
    "Bangalore",
    "Kolkata"
]

REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


# ================================
# LOGGING CONFIGURATION
# ================================

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"
ALERT_LOG_FILE = LOG_DIR / "alerts.log"

LOG_LEVEL = "INFO"


# ================================
# ALERT SYSTEM CONFIGURATION
# ================================

ALERT_THRESHOLDS = {
    "temperature_high": 30,
    "temperature_low": 10,
    "humidity_high": 80,
    "wind_speed_high": 15
}

ENABLE_ALERTS = True


# ================================
# REPORTING CONFIGURATION
# ================================

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

REPORT_FILE = REPORT_DIR / "weather_report.txt"


# ================================
# DASHBOARD CONFIGURATION
# ================================

DASHBOARD_HOST = "localhost"
DASHBOARD_PORT = 8501

AUTO_REFRESH_INTERVAL = 60  # seconds


# ================================
# SCHEDULER CONFIGURATION
# ================================

SCHEDULE_INTERVAL_MINUTES = 30


# ================================
# MONITORING CONFIGURATION
# ================================

HEALTH_CHECK_ENABLED = True
MAX_FAILURE_THRESHOLD = 5


# ================================
# BACKUP CONFIGURATION
# ================================

BACKUP_DIR = DATABASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

BACKUP_ENABLED = True


# ================================
# ENVIRONMENT FLAGS
# ================================

ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"