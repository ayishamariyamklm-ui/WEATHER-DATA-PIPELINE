import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from config.config import ALERT_THRESHOLDS, ENABLE_ALERTS
from src.database import insert_alert

logger = logging.getLogger(__name__)


# ================================
# CHECK ALERT CONDITIONS
# ================================

def check_alerts(data: dict) -> int:
    """
    Check all alert conditions for a weather record.
    Returns number of alerts triggered.
    """

    if not ENABLE_ALERTS:
        return 0

    alert_count = 0

    city = data["city"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    wind_speed = data["wind_speed"]

    # ================================
    # TEMPERATURE HIGH
    # ================================

    if temperature is not None and temperature > ALERT_THRESHOLDS["temperature_high"]:
        message = f"High temperature detected: {temperature}°C"
        trigger_alert(city, "High Temperature", temperature,
                      ALERT_THRESHOLDS["temperature_high"], message)
        alert_count += 1

    # ================================
    # TEMPERATURE LOW
    # ================================

    if temperature is not None and temperature < ALERT_THRESHOLDS["temperature_low"]:
        message = f"Low temperature detected: {temperature}°C"
        trigger_alert(city, "Low Temperature", temperature,
                      ALERT_THRESHOLDS["temperature_low"], message)
        alert_count += 1

    # ================================
    # HUMIDITY HIGH
    # ================================

    if humidity is not None and humidity > ALERT_THRESHOLDS["humidity_high"]:
        message = f"High humidity detected: {humidity}%"
        trigger_alert(city, "High Humidity", humidity,
                      ALERT_THRESHOLDS["humidity_high"], message)
        alert_count += 1

    # ================================
    # WIND SPEED HIGH
    # ================================

    if wind_speed is not None and wind_speed > ALERT_THRESHOLDS["wind_speed_high"]:
        message = f"High wind speed detected: {wind_speed} m/s"
        trigger_alert(city, "High Wind Speed", wind_speed,
                      ALERT_THRESHOLDS["wind_speed_high"], message)
        alert_count += 1

    return alert_count


# ================================
# TRIGGER ALERT
# ================================

def trigger_alert(city, alert_type, value, threshold, message):
    """
    Save alert and log it
    """

    try:
        insert_alert(city, alert_type, value, threshold, message)

        logger.warning(
            f"ALERT: {alert_type} | City: {city} | Value: {value} | Threshold: {threshold}"
        )

    except Exception as e:
        logger.error(f"Failed to trigger alert: {e}")