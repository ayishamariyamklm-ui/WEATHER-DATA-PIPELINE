import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
import logging
from datetime import datetime, UTC

from config.config import DB_PATH

logger = logging.getLogger(__name__)


# ================================
# DATABASE CONNECTION
# ================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ================================
# INSERT WEATHER DATA
# ================================

def insert_weather_data(data: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO weather_data (
            city, temperature, humidity, pressure,
            wind_speed, weather_condition, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            data["city"],
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["wind_speed"],
            data["weather_condition"],
            data["timestamp"]
        ))

        conn.commit()
        conn.close()

        logger.info(f"Weather data inserted for {data['city']}")

    except Exception as e:
        logger.error(f"Failed to insert weather data: {e}")
        log_error("database.insert_weather_data", str(e))


# ================================
# INSERT ALERT
# ================================

def insert_alert(city, alert_type, value, threshold, message):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO alerts (
            city, alert_type, alert_value, threshold,
            message, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            city,
            alert_type,
            value,
            threshold,
            message,
            datetime.now(UTC).isoformat()
        ))

        conn.commit()
        conn.close()

        logger.warning(f"Alert inserted: {alert_type} for {city}")

    except Exception as e:
        logger.error(f"Failed to insert alert: {e}")
        log_error("database.insert_alert", str(e))


# ================================
# PIPELINE RUN TRACKING
# ================================

def insert_pipeline_run(start_time, end_time, status,
                        total_cities, success_count,
                        failure_count, alert_count, duration):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO pipeline_runs (
            start_time, end_time, status,
            total_cities, success_count,
            failure_count, alert_count, duration
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            start_time,
            end_time,
            status,
            total_cities,
            success_count,
            failure_count,
            alert_count,
            duration
        ))

        conn.commit()
        conn.close()

        logger.info("Pipeline run logged successfully")

    except Exception as e:
        logger.error(f"Failed to log pipeline run: {e}")


# ================================
# ERROR LOGGING
# ================================

def log_error(module, error_message):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO errors (
            module, error_message, timestamp
        )
        VALUES (?, ?, ?)
        """

        cursor.execute(query, (
            module,
            error_message,
            datetime.now(UTC).isoformat()
        ))

        conn.commit()
        conn.close()

    except Exception as e:
        logger.error(f"Failed to log error to database: {e}")


# ================================
# FETCH DATA (FOR DASHBOARD)
# ================================

def fetch_weather_data(limit=100):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM weather_data
        ORDER BY timestamp DESC
        LIMIT ?
        """

        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        conn.close()
        return rows

    except Exception as e:
        logger.error(f"Failed to fetch weather data: {e}")
        return []


def fetch_alerts(limit=50):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM alerts
        ORDER BY timestamp DESC
        LIMIT ?
        """

        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        conn.close()
        return rows

    except Exception as e:
        logger.error(f"Failed to fetch alerts: {e}")
        return []