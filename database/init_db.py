import sqlite3
import logging
from pathlib import Path

# Import config
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import DB_PATH, SCHEMA_PATH
from src.logger import setup_logger


# ================================
# SETUP LOGGER
# ================================

setup_logger()
logger = logging.getLogger(__name__)


# ================================
# INITIALIZE DATABASE
# ================================

def initialize_database():
    try:
        logger.info("Initializing database...")

        # Ensure database directory exists
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Connect to SQLite DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        logger.info(f"Connected to database at {DB_PATH}")

        # Read schema.sql
        if not Path(SCHEMA_PATH).exists():
            raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # Execute schema
        cursor.executescript(schema_sql)

        conn.commit()
        logger.info("Database schema applied successfully")

        # Verify tables
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table';
        """)
        tables = cursor.fetchall()

        logger.info(f"Tables created: {[table[0] for table in tables]}")

        conn.close()
        logger.info("Database initialization completed")

        print("\nDatabase initialized successfully!")
        print(f"Database location: {DB_PATH}")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

        print("\nDatabase initialization FAILED")
        print(f"Error: {e}")


# ================================
# RUN SCRIPT
# ================================

if __name__ == "__main__":
    initialize_database()