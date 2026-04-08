import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock

from src.api_client import fetch_weather


# ================================
# MOCK SUCCESS RESPONSE
# ================================

@patch("src.api_client.requests.get")
def test_fetch_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "main": {
            "temp": 300.15,   # Kelvin
            "humidity": 70
        }
    }

    mock_get.return_value = mock_response

    result = fetch_weather("Mumbai")

    assert result is not None
    assert result["city"] == "Mumbai"
    assert "temperature" in result
    assert "humidity" in result


# ================================
# API FAILURE TEST
# ================================

@patch("src.api_client.requests.get")
def test_fetch_weather_api_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500

    mock_get.return_value = mock_response

    result = fetch_weather("Delhi")

    assert result is None


# ================================
# INVALID JSON RESPONSE
# ================================

@patch("src.api_client.requests.get")
def test_fetch_weather_invalid_json(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = Exception("Invalid JSON")

    mock_get.return_value = mock_response

    result = fetch_weather("Chennai")

    assert result is None


# ================================
# NETWORK ERROR TEST
# ================================

@patch("src.api_client.requests.get")
def test_fetch_weather_network_error(mock_get):
    mock_get.side_effect = Exception("Network error")

    result = fetch_weather("Bangalore")

    assert result is None


# ================================
# EDGE CASE: EMPTY RESPONSE
# ================================

@patch("src.api_client.requests.get")
def test_fetch_weather_empty_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    mock_get.return_value = mock_response

    result = fetch_weather("Kolkata")

    assert result is None


# ================================
# TEMPERATURE CONVERSION CHECK
# ================================

@patch("src.api_client.requests.get")
def test_temperature_conversion(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "main": {
            "temp": 273.15,   # 0°C
            "humidity": 50
        }
    }

    mock_get.return_value = mock_response

    result = fetch_weather("TestCity")

    assert result is not None
    assert abs(result["temperature"] - 0) < 0.1
    assert result["humidity"] == 50