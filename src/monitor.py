import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import logging
from datetime import datetime, UTC

from src.database import get_connection
from config.config import MONITOR_INTERVAL, HEALTH_CHECK_THRESHOLD

logger = logging.getLogger(__name__)


# ================================
# DATABASE HEALTH CHECK
# ================================

def check_database_connection():
    """
    Check if database connection is working
    """
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        logger.info("Database connection is healthy")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


# ================================
# DATA FRESHNESS CHECK
# ================================

def check_data_freshness():
    """
    Check if latest data is recent enough
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(timestamp) FROM weather_data
        """)
        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            last_timestamp = datetime.fromisoformat(result[0])
            current_time = datetime.now(UTC)

            diff = (current_time - last_timestamp).total_seconds()

            if diff > HEALTH_CHECK_THRESHOLD:
                logger.warning(
                    f"Data is stale. Last update was {diff:.2f} seconds ago"
                )
                return False
            else:
                logger.info("Data freshness check passed")
                return True
        else:
            logger.warning("No data found in database")
            return False

    except Exception as e:
        logger.error(f"Error checking data freshness: {e}")
        return False


# ================================
# ALERT COUNT CHECK
# ================================

def check_recent_alerts():
    """
    Check number of alerts generated recently
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM alerts
            WHERE timestamp >= datetime('now', '-1 hour')
        """)
        count = cursor.fetchone()[0]
        conn.close()

        logger.info(f"Alerts in last 1 hour: {count}")
        return count

    except Exception as e:
        logger.error(f"Error checking alerts: {e}")
        return 0


# ================================
# SYSTEM HEALTH SUMMARY
# ================================

def system_health_check():
    """
    Perform full system health check
    """
    logger.info("Running system health check")

    db_status = check_database_connection()
    data_status = check_data_freshness()
    alert_count = check_recent_alerts()

    health_status = {
        "database": db_status,
        "data_freshness": data_status,
        "recent_alerts": alert_count,
        "timestamp": datetime.now(UTC).isoformat()
    }

    if not db_status or not data_status:
        logger.warning("System health check FAILED")
    else:
        logger.info("System health check PASSED")

    return health_status


# ================================
# REAL-TIME MONITOR LOOP
# ================================

def start_monitoring():
    """
    Continuous monitoring loop
    """
    logger.info("Starting real-time monitoring service")

    while True:
        try:
            health = system_health_check()

            print("\n--- SYSTEM HEALTH ---")
            print(f"Time: {health['timestamp']}")
            print(f"Database: {health['database']}")
            print(f"Data Freshness: {health['data_freshness']}")
            print(f"Recent Alerts: {health['recent_alerts']}")

            time.sleep(MONITOR_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
            print("\nMonitoring stopped")
            break

        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            time.sleep(MONITOR_INTERVAL)