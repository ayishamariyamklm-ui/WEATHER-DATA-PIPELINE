import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.reporter import generate_report
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
    print("\n=== GENERATING WEATHER REPORT ===\n")

    try:
        logger.info("Report generation started")

        generate_report()

        logger.info("Report generation completed successfully")

        print("\nReport generated successfully")

    except Exception as e:
        logger.error(f"Report generation failed: {e}")

        print("\n=== REPORT GENERATION FAILED ===")
        print(f"Error: {e}")


# ================================
# RUN SCRIPT
# ================================

if __name__ == "__main__":
    main()