import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# ================================
# BASIC FIELD VALIDATORS
# ================================

def validate_city(city):
    if not city or not isinstance(city, str):
        raise ValueError("Invalid city name")
    return city.strip()


def validate_temperature(temp):
    if temp is None:
        raise ValueError("Temperature is missing")

    if not (-100 <= temp <= 100):
        raise ValueError(f"Invalid temperature value: {temp}")

    return float(temp)


def validate_humidity(humidity):
    if humidity is None:
        raise ValueError("Humidity is missing")

    if not (0 <= humidity <= 100):
        raise ValueError(f"Invalid humidity value: {humidity}")

    return float(humidity)


def validate_pressure(pressure):
    if pressure is None:
        raise ValueError("Pressure is missing")

    if not (800 <= pressure <= 1200):
        raise ValueError(f"Invalid pressure value: {pressure}")

    return float(pressure)


def validate_wind_speed(speed):
    if speed is None:
        raise ValueError("Wind speed is missing")

    if not (0 <= speed <= 100):
        raise ValueError(f"Invalid wind speed: {speed}")

    return float(speed)


def validate_weather_condition(condition):
    if not condition or not isinstance(condition, str):
        return "Unknown"
    return condition.strip()


def validate_timestamp(timestamp):
    if not timestamp:
        raise ValueError("Timestamp is missing")

    try:
        # Accept ISO8601 and flexible formats
        parsed_time = datetime.fromisoformat(timestamp)
        return parsed_time.isoformat()
    except Exception:
        try:
            parsed_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return parsed_time.isoformat()
        except Exception:
            raise ValueError(f"Invalid timestamp format: {timestamp}")


# ================================
# FULL RECORD VALIDATION
# ================================

def validate_weather_data(data: dict) -> dict:
    """
    Validate full weather record before DB insert
    """

    try:
        validated_data = {
            "city": validate_city(data.get("city")),
            "temperature": validate_temperature(data.get("temperature")),
            "humidity": validate_humidity(data.get("humidity")),
            "pressure": validate_pressure(data.get("pressure")),
            "wind_speed": validate_wind_speed(data.get("wind_speed")),
            "weather_condition": validate_weather_condition(data.get("weather_condition")),
            "timestamp": validate_timestamp(data.get("timestamp")),
        }

        logger.info(f"Validation successful for {validated_data['city']}")

        return validated_data

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise


# ================================
# BULK VALIDATION (ADVANCED)
# ================================

def validate_bulk_data(data_list):
    """
    Validate multiple records safely
    Returns only valid records
    """

    valid_records = []
    failed_records = 0

    for data in data_list:
        try:
            valid_data = validate_weather_data(data)
            valid_records.append(valid_data)
        except Exception as e:
            failed_records += 1
            logger.warning(f"Skipping invalid record: {e}")

    logger.info(
        f"Bulk validation completed | Valid: {len(valid_records)} | Failed: {failed_records}"
    )

    return valid_records