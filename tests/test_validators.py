import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.validators import (
    validate_temperature,
    validate_humidity,
    validate_weather_data
)


# ================================
# TEMPERATURE TESTS
# ================================

def test_valid_temperature():
    assert validate_temperature(25) is True
    assert validate_temperature(0) is True
    assert validate_temperature(50) is True


def test_invalid_temperature():
    assert validate_temperature(-100) is False
    assert validate_temperature(100) is False
    assert validate_temperature(None) is False


# ================================
# HUMIDITY TESTS
# ================================

def test_valid_humidity():
    assert validate_humidity(50) is True
    assert validate_humidity(0) is True
    assert validate_humidity(100) is True


def test_invalid_humidity():
    assert validate_humidity(-10) is False
    assert validate_humidity(150) is False
    assert validate_humidity(None) is False


# ================================
# FULL DATA VALIDATION TESTS
# ================================

def test_valid_weather_data():
    valid_data = {
        "city": "Mumbai",
        "temperature": 30,
        "humidity": 70
    }

    assert validate_weather_data(valid_data) is True


def test_missing_fields():
    invalid_data = {
        "city": "Delhi",
        "temperature": 28
    }

    assert validate_weather_data(invalid_data) is False


def test_invalid_values():
    invalid_data = {
        "city": "Chennai",
        "temperature": 200,
        "humidity": -5
    }

    assert validate_weather_data(invalid_data) is False


def test_empty_data():
    assert validate_weather_data({}) is False
    assert validate_weather_data(None) is False


# ================================
# EDGE CASES
# ================================

def test_boundary_temperature():
    assert validate_temperature(-50) is True
    assert validate_temperature(60) is True


def test_boundary_humidity():
    assert validate_humidity(0) is True
    assert validate_humidity(100) is True