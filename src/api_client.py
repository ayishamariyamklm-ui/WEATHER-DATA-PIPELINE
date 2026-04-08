import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import time
import logging
from datetime import datetime, UTC

from config.config import (
    API_KEY,
    BASE_URL,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
)

from src.validators import validate_weather_data

logger = logging.getLogger(__name__)


# ================================
# FETCH WEATHER DATA
# ================================

def fetch_weather(city: str) -> dict:
    """
    Fetch weather data for a given city with retry logic
    """

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Fetching weather data for {city} (Attempt {attempt + 1})")

            response = requests.get(
                BASE_URL,
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            # Raise error if bad response
            response.raise_for_status()

            data = response.json()

            # Transform API response
            weather_data = transform_weather_data(data, city)

            # Validate data
            validated_data = validate_weather_data(weather_data)

            logger.info(f"Successfully fetched data for {city}")

            return validated_data

        except requests.exceptions.RequestException as e:
            logger.warning(f"API request failed for {city}: {e}")

        except Exception as e:
            logger.error(f"Processing failed for {city}: {e}")
            break

        # Retry delay
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)

    logger.error(f"All retries failed for {city}")
    raise Exception(f"Failed to fetch weather data for {city}")


# ================================
# TRANSFORM DATA
# ================================

def transform_weather_data(api_data: dict, city: str) -> dict:
    """
    Transform raw API response into structured format
    """

    try:
        main_data = api_data.get("main", {})
        wind_data = api_data.get("wind", {})
        weather_info = api_data.get("weather", [{}])[0]

        transformed = {
            "city": city,
            "temperature": main_data.get("temp"),
            "humidity": main_data.get("humidity"),
            "pressure": main_data.get("pressure"),
            "wind_speed": wind_data.get("speed"),
            "weather_condition": weather_info.get("description"),
            "timestamp": datetime.now(UTC).isoformat()
        }

        return transformed

    except Exception as e:
        logger.error(f"Data transformation failed for {city}: {e}")
        raise