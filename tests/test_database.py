import pytest
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import (
    get_connection,
    insert_weather_data,
    insert_alert
)


# ================================
# TEST DATABASE SETUP (TEMP DB)
# ================================

TEST_DB = "test_weather.db"


@pytest.fixture(scope="module")
def setup_test_db():
    # Create temporary database
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            alert_type TEXT,
            value REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

    yield

    # Cleanup after tests
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# ================================
# MOCK CONNECTION
# ================================

@pytest.fixture
def mock_connection(monkeypatch):
    def _mock_conn():
        return sqlite3.connect(TEST_DB)

    monkeypatch.setattr("src.database.get_connection", _mock_conn)


# ================================
# INSERT WEATHER DATA TEST
# ================================

def test_insert_weather_data(setup_test_db, mock_connection):
    data = {
        "city": "Mumbai",
        "temperature": 30,
        "humidity": 70,
        "timestamp": "2026-01-01T10:00:00"
    }

    insert_weather_data(data)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather_data WHERE city = 'Mumbai'")
    result = cursor.fetchone()

    conn.close()

    assert result is not None
    assert result[1] == "Mumbai"
    assert result[2] == 30


# ================================
# INSERT ALERT TEST
# ================================

def test_insert_alert(setup_test_db, mock_connection):
    insert_alert("Delhi", "High Temperature", 40)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alerts WHERE city = 'Delhi'")
    result = cursor.fetchone()

    conn.close()

    assert result is not None
    assert result[1] == "Delhi"
    assert result[2] == "High Temperature"


# ================================
# MULTIPLE INSERT TEST
# ================================

def test_multiple_inserts(setup_test_db, mock_connection):
    for i in range(3):
        data = {
            "city": f"City{i}",
            "temperature": 25 + i,
            "humidity": 60 + i,
            "timestamp": f"2026-01-01T10:0{i}:00"
        }
        insert_weather_data(data)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM weather_data")
    count = cursor.fetchone()[0]

    conn.close()

    assert count >= 3


# ================================
# EDGE CASE: EMPTY DATA
# ================================

def test_insert_empty_data(setup_test_db, mock_connection):
    with pytest.raises(Exception):
        insert_weather_data({})


# ================================
# EDGE CASE: INVALID DATA TYPES
# ================================

def test_invalid_data_types(setup_test_db, mock_connection):
    data = {
        "city": "Test",
        "temperature": "invalid",
        "humidity": "invalid",
        "timestamp": "invalid"
    }

    with pytest.raises(Exception):
        insert_weather_data(data)