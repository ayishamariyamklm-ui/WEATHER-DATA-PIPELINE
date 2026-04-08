import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import shutil
import logging
from datetime import datetime, UTC

from config.config import DATABASE_PATH
from src.logger import setup_logger


# ================================
# SETUP LOGGER
# ================================

setup_logger()
logger = logging.getLogger(__name__)


# ================================
# CONFIG
# ================================

BACKUP_DIR = os.path.join(os.path.dirname(DATABASE_PATH), "backups")


# ================================
# BACKUP FUNCTION
# ================================

def create_backup():
    """Create a timestamped backup of the database"""

    try:
        # Ensure backup directory exists
        os.makedirs(BACKUP_DIR, exist_ok=True)

        # Generate timestamp
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

        # Backup file name
        backup_filename = f"weather_backup_{timestamp}.db"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        # Copy database file
        shutil.copy2(DATABASE_PATH, backup_path)

        logger.info(f"Database backup created: {backup_path}")
        print(f"Backup successful: {backup_path}")

    except FileNotFoundError:
        logger.error("Database file not found. Run setup_database first.")
        print("Backup failed: Database file not found")

    except Exception as e:
        logger.error(f"Backup failed: {e}")
        print(f"Backup failed: {e}")


# ================================
# CLEAN OLD BACKUPS
# ================================

def clean_old_backups(retention_days=7):
    """Delete backups older than retention period"""

    try:
        if not os.path.exists(BACKUP_DIR):
            return

        now = datetime.now(UTC)

        for file in os.listdir(BACKUP_DIR):
            file_path = os.path.join(BACKUP_DIR, file)

            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(
                    os.path.getmtime(file_path), UTC
                )

                age_days = (now - file_mtime).days

                if age_days > retention_days:
                    os.remove(file_path)
                    logger.info(f"Deleted old backup: {file}")
                    print(f"Deleted old backup: {file}")

    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        print(f"Cleanup failed: {e}")


# ================================
# MAIN FUNCTION
# ================================

def main():
    print("\n=== DATABASE BACKUP STARTED ===\n")

    create_backup()
    clean_old_backups(retention_days=7)

    print("\n=== BACKUP PROCESS COMPLETED ===\n")


# ================================
# RUN SCRIPT
# ================================

if __name__ == "__main__":
    main()