import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import logging
from datetime import datetime, UTC

from src.etl_pipeline import run_pipeline
from config.config import SCHEDULER_INTERVAL, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)


# ================================
# PIPELINE EXECUTION WITH RETRIES
# ================================

def run_with_retries():
    """
    Run pipeline with retry mechanism
    """
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            logger.info(f"Starting pipeline attempt {attempt + 1}")

            start_time = time.time()
            run_pipeline()
            duration = time.time() - start_time

            logger.info(f"Pipeline completed successfully in {duration:.2f} seconds")
            return True

        except Exception as e:
            attempt += 1
            logger.error(f"Pipeline failed on attempt {attempt}: {e}")

            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached. Pipeline execution failed.")
                return False


# ================================
# SCHEDULER LOOP
# ================================

def start_scheduler():
    """
    Run pipeline at fixed intervals
    """
    logger.info("Starting scheduler service")

    while True:
        try:
            current_time = datetime.now(UTC).isoformat()
            logger.info(f"Scheduler triggered at {current_time}")

            success = run_with_retries()

            if success:
                logger.info("Scheduled pipeline run completed successfully")
            else:
                logger.warning("Scheduled pipeline run failed")

            logger.info(f"Sleeping for {SCHEDULER_INTERVAL} seconds\n")
            time.sleep(SCHEDULER_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            print("\nScheduler stopped")
            break

        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(SCHEDULER_INTERVAL)


# ===============
# SINGLE RUN 
# ===============

def run_once():
    """
    Run pipeline once (useful for testing)
    """
    logger.info("Running scheduler in single-run mode")
    run_with_retries()