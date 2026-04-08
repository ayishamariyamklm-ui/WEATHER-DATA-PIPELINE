import sys
import os
import logging
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logger import setup_logger
from database.init_db import initialize_database


# ================================
# SETUP LOGGER
# ================================

setup_logger()
logger = logging.getLogger(__name__)


# ================================
# MAIN FUNCTION
# ================================

def main():
    print("\n=== DATABASE SETUP STARTED ===\n")

    start_time = time.time()

    try:
        logger.info("Starting database setup process")

        # Initialize database
        initialize_database()

        duration = time.time() - start_time

        logger.info(f"Database setup completed in {duration:.2f} seconds")

        print("\n=== DATABASE SETUP COMPLETED ===")
        print(f"Duration: {duration:.2f} seconds")

    except Exception as e:
        logger.error(f"Database setup failed: {e}")

        print("\n=== DATABASE SETUP FAILED ===")
        print(f"Error: {e}")


# ================================
# RUN SCRIPT
# ================================

if __name__ == "__main__":
    main()
