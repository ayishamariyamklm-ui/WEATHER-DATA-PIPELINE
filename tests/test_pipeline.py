import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch

from src.etl_pipeline import run_pipeline


# ================================
# MOCK SUCCESS FLOW
# ================================

@patch("src.etl_pipeline.insert_alert")
@patch("src.etl_pipeline.insert_weather_data")
@patch("src.etl_pipeline.fetch_weather")
def test_pipeline_success(mock_fetch, mock_insert, mock_alert):
    # Mock API response
    mock_fetch.return_value = {
        "city": "Mumbai",
        "temperature": 30,
        "humidity": 70,
        "timestamp": "2026-01-01T10:00:00"
    }

    run_pipeline()

    # Verify functions called
    assert mock_fetch.called
    assert mock_insert.called


# ================================
# MOCK FAILURE FLOW (API FAIL)
# ================================

@patch("src.etl_pipeline.insert_weather_data")
@patch("src.etl_pipeline.fetch_weather")
def test_pipeline_api_failure(mock_fetch, mock_insert):
    # Simulate API failure
    mock_fetch.return_value = None

    run_pipeline()

    # Insert should NOT be called
    assert not mock_insert.called


# ================================
# MOCK ALERT TRIGGER
# ================================

@patch("src.etl_pipeline.insert_alert")
@patch("src.etl_pipeline.insert_weather_data")
@patch("src.etl_pipeline.fetch_weather")
def test_pipeline_alert_trigger(mock_fetch, mock_insert, mock_alert):
    # High temperature triggers alert
    mock_fetch.return_value = {
        "city": "Delhi",
        "temperature": 45,
        "humidity": 20,
        "timestamp": "2026-01-01T10:00:00"
    }

    run_pipeline()

    assert mock_insert.called
    assert mock_alert.called


# ================================
# MULTIPLE CITY PROCESSING
# ================================

@patch("src.etl_pipeline.insert_weather_data")
@patch("src.etl_pipeline.fetch_weather")
def test_pipeline_multiple_cities(mock_fetch, mock_insert):
    # Return different data each call
    mock_fetch.side_effect = [
        {"city": "Mumbai", "temperature": 30, "humidity": 70, "timestamp": "2026-01-01T10:00:00"},
        {"city": "Delhi", "temperature": 35, "humidity": 60, "timestamp": "2026-01-01T10:00:00"},
        {"city": "Chennai", "temperature": 33, "humidity": 80, "timestamp": "2026-01-01T10:00:00"},
        {"city": "Bangalore", "temperature": 28, "humidity": 75, "timestamp": "2026-01-01T10:00:00"},
        {"city": "Kolkata", "temperature": 32, "humidity": 85, "timestamp": "2026-01-01T10:00:00"},
    ]

    run_pipeline()

    # Should insert for each successful fetch
    assert mock_insert.call_count >= 1


# ================================
# EDGE CASE: PARTIAL FAILURES
# ================================

@patch("src.etl_pipeline.insert_weather_data")
@patch("src.etl_pipeline.fetch_weather")
def test_pipeline_partial_failures(mock_fetch, mock_insert):
    # Some calls fail
    mock_fetch.side_effect = [
        None,
        {"city": "Delhi", "temperature": 35, "humidity": 60, "timestamp": "2026-01-01T10:00:00"},
        None,
    ]

    run_pipeline()

    # Only successful ones should be inserted
    assert mock_insert.call_count == 1


# ================================
# EDGE CASE: EMPTY DATA
# ================================

@patch("src.etl_pipeline.fetch_weather")
def test_pipeline_all_failures(mock_fetch):
    mock_fetch.return_value = None

    # Should not crash
    run_pipeline()

    assert mock_fetch.called