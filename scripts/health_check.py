import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
import logging
from datetime import datetime, UTC

from config.config import DATABASE_PATH
from src.logger import setup_logger


# ================================
# SETUP LOGGER
# ================================

setup_logger()
logger = logging.getLogger(__name__)


# ================================
# HEALTH CHECK FUNCTIONS
# ================================

def check_database_connection():
    """Check if database is accessible"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.close()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def check_tables_exist():
    """Check required tables exist"""
    required_tables = ["weather_data", "alerts"]

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        tables = [row[0] for row in cursor.fetchall()]

        conn.close()

        missing = [t for t in required_tables if t not in tables]

        if missing:
            logger.error(f"Missing tables: {missing}")
            return False

        logger.info("All required tables exist")
        return True

    except Exception as e:
        logger.error(f"Table check failed: {e}")
        return False


def check_recent_data():
    """Check if recent weather data exists (last 1 hour)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM weather_data
            WHERE timestamp >= datetime('now', '-1 hour')
        """)

        count = cursor.fetchone()[0]
        conn.close()

        if count == 0:
            logger.warning("No recent weather data found (last 1 hour)")
            return False

        logger.info(f"Recent data available: {count} records")
        return True

    except Exception as e:
        logger.error(f"Recent data check failed: {e}")
        return False


def check_alerts():
    """Check if alerts system is working"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM alerts
            WHERE timestamp >= datetime('now', '-24 hour')
        """)

        count = cursor.fetchone()[0]
        conn.close()

        logger.info(f"Alerts in last 24h: {count}")
        return True

    except Exception as e:
        logger.error(f"Alerts check failed: {e}")
        return False


# ================================
# MAIN HEALTH CHECK
# ================================

def run_health_check():
    print("\n=== SYSTEM HEALTH CHECK ===\n")

    results = {
        "database_connection": check_database_connection(),
        "tables_exist": check_tables_exist(),
        "recent_data": check_recent_data(),
        "alerts": check_alerts()
    }

    print("\n--- HEALTH CHECK RESULTS ---")

    all_ok = True

    for check, status in results.items():
        status_text = "OK" if status else "FAIL"
        print(f"{check}: {status_text}")

        if not status:
            all_ok = False

    print("\n----------------------------")

    if all_ok:
        print("SYSTEM STATUS: HEALTHY")
        logger.info("System health check passed")
    else:
        print("SYSTEM STATUS: ISSUES DETECTED")
        logger.warning("System health check found issues")

    print(f"Checked at: {datetime.now(UTC).isoformat()}\n")


# ================================
# RUN SCRIPT
# ================================

if __name__ == "__main__":
    run_health_check()