import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import time
from datetime import datetime, UTC

from config.config import CITIES
from src.api_client import fetch_weather
from src.database import (
    insert_weather_data,
    insert_pipeline_run,
    log_error
)
from src.alerts import check_alerts

logger = logging.getLogger(__name__)


# ================================
# RUN PIPELINE
# ================================

def run_pipeline():
    """
    Main ETL pipeline execution
    """

    logger.info("Starting ETL pipeline run")

    start_time = time.time()
    start_timestamp = datetime.now(UTC).isoformat()

    total_cities = len(CITIES)
    success_count = 0
    failure_count = 0
    alert_count = 0

    try:
        for city in CITIES:
            try:
                logger.info(f"Processing city: {city}")

                # ================================
                # EXTRACT + TRANSFORM + VALIDATE
                # ================================

                data = fetch_weather(city)

                # ================================
                # LOAD TO DATABASE
                # ================================

                insert_weather_data(data)
                success_count += 1

                # ================================
                # ALERT CHECK
                # ================================

                alerts_triggered = check_alerts(data)
                alert_count += alerts_triggered

            except Exception as e:
                failure_count += 1
                logger.error(f"Failed for {city}: {e}")
                log_error("etl_pipeline.run_pipeline", f"{city}: {e}")

        # ================================
        # PIPELINE SUMMARY
        # ================================

        end_time = time.time()
        duration = end_time - start_time
        end_timestamp = datetime.now(UTC).isoformat()

        status = "SUCCESS" if failure_count == 0 else "PARTIAL_SUCCESS"

        summary_message = (
            f"Pipeline completed | Success: {success_count}, "
            f"Failures: {failure_count}, Alerts: {alert_count}, "
            f"Duration: {duration:.2f}s"
        )

        logger.info(summary_message)

        # ================================
        # LOG PIPELINE RUN
        # ================================

        insert_pipeline_run(
            start_time=start_timestamp,
            end_time=end_timestamp,
            status=status,
            total_cities=total_cities,
            success_count=success_count,
            failure_count=failure_count,
            alert_count=alert_count,
            duration=duration
        )

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")

        end_timestamp = datetime.now(UTC).isoformat()

        insert_pipeline_run(
            start_time=start_timestamp,
            end_time=end_timestamp,
            status="FAILED",
            total_cities=total_cities,
            success_count=success_count,
            failure_count=failure_count,
            alert_count=alert_count,
            duration=0
        )

        raise