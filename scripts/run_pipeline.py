import sys
import os
import time
import logging
from datetime import datetime, UTC

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.etl_pipeline import run_pipeline
from src.logger import setup_logger


# ================================
# SETUP LOGGER
# ================================

setup_logger()
logger = logging.getLogger(__name__)


# ================================
# MAIN FUNCTION
# ================================

def main():
    print("\n=== STARTING WEATHER DATA PIPELINE ===\n")

    start_time = time.time()
    start_timestamp = datetime.now(UTC).isoformat()

    try:
        logger.info("Pipeline execution started")

        # Run ETL pipeline
        run_pipeline()

        end_time = time.time()
        duration = end_time - start_time

        logger.info(f"Pipeline completed in {duration:.2f} seconds")

        print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Start Time (UTC): {start_timestamp}")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")

        print("\n=== PIPELINE FAILED ===")
        print(f"Error: {e}")


# ================================
# RUN SCRIPT
# ================================

if __name__ == "__main__":
    main()