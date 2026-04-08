import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from datetime import datetime, UTC

from src.database import get_connection
from config.config import REPORT_FILE

logger = logging.getLogger(__name__)


# ================================
# FETCH DATA
# ================================

def fetch_weather_summary():
    """
    Get aggregated weather data summary
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT city,
                   COUNT(*) as records,
                   AVG(temperature) as avg_temp,
                   MAX(temperature) as max_temp,
                   MIN(temperature) as min_temp,
                   AVG(humidity) as avg_humidity
            FROM weather_data
            GROUP BY city
        """)

        data = cursor.fetchall()
        conn.close()

        return data

    except Exception as e:
        logger.error(f"Error fetching weather summary: {e}")
        return []


def fetch_alert_summary():
    """
    Get alert statistics
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT alert_type,
                   COUNT(*) as count
            FROM alerts
            GROUP BY alert_type
        """)

        data = cursor.fetchall()
        conn.close()

        return data

    except Exception as e:
        logger.error(f"Error fetching alert summary: {e}")
        return []


# ================================
# GENERATE REPORT CONTENT
# ================================

def generate_report_content():
    """
    Create formatted report text
    """
    weather_data = fetch_weather_summary()
    alert_data = fetch_alert_summary()

    report_lines = []

    report_lines.append("WEATHER DATA PIPELINE REPORT")
    report_lines.append("=" * 40)
    report_lines.append(f"Generated at: {datetime.now(UTC).isoformat()}\n")

    # Weather Summary
    report_lines.append("Weather Summary (City-wise)")
    report_lines.append("-" * 40)

    if weather_data:
        for row in weather_data:
            city, records, avg_temp, max_temp, min_temp, avg_humidity = row

            report_lines.append(f"City: {city}")
            report_lines.append(f"  Records: {records}")
            report_lines.append(f"  Avg Temp: {avg_temp:.2f} C")
            report_lines.append(f"  Max Temp: {max_temp:.2f} C")
            report_lines.append(f"  Min Temp: {min_temp:.2f} C")
            report_lines.append(f"  Avg Humidity: {avg_humidity:.2f}%\n")
    else:
        report_lines.append("No weather data available\n")

    # Alert Summary
    report_lines.append("Alert Summary")
    report_lines.append("-" * 40)

    if alert_data:
        for row in alert_data:
            alert_type, count = row
            report_lines.append(f"{alert_type}: {count}")
    else:
        report_lines.append("No alerts generated")

    report_lines.append("\nEnd of Report")
    report_lines.append("=" * 40)

    return "\n".join(report_lines)


# ================================
# SAVE REPORT
# ================================

def save_report():
    """
    Generate and save report to file
    """
    try:
        report_content = generate_report_content()

        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write(report_content)

        logger.info(f"Report generated and saved to {REPORT_FILE}")
        print(f"Report saved to {REPORT_FILE}")

    except Exception as e:
        logger.error(f"Error saving report: {e}")
        print(f"Failed to generate report: {e}")


# ================================
# MAIN FUNCTION
# ================================

def generate_report():
    """
    Public function to generate report
    """
    logger.info("Generating weather report")
    save_report()