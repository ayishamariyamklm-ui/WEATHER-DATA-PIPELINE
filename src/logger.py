import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import sys
from logging.handlers import RotatingFileHandler
from config.config import LOG_FILE, ERROR_LOG_FILE, ALERT_LOG_FILE, LOG_LEVEL


# ================================
# CUSTOM FORMATTER (SAFE UTF-8)
# ================================

class SafeFormatter(logging.Formatter):
    def format(self, record):
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = record.msg.encode("utf-8", errors="ignore").decode("utf-8")
            return super().format(record)


# ================================
# SETUP LOGGER
# ================================

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # Prevent duplicate handlers
    if logger.handlers:
        return

    formatter = SafeFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # ================================
    # CONSOLE HANDLER (UTF-8 SAFE)
    # ================================

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ================================
    # FILE HANDLER (MAIN LOG)
    # ================================

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ================================
    # ERROR LOG HANDLER
    # ================================

    error_handler = RotatingFileHandler(
        ERROR_LOG_FILE,
        maxBytes=2 * 1024 * 1024,
        backupCount=2,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # ================================
    # ALERT LOG HANDLER
    # ================================

    alert_handler = RotatingFileHandler(
        ALERT_LOG_FILE,
        maxBytes=2 * 1024 * 1024,
        backupCount=2,
        encoding="utf-8"
    )
    alert_handler.setLevel(logging.WARNING)
    alert_handler.setFormatter(formatter)

    # ================================
    # ADD HANDLERS
    # ================================

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(alert_handler)

    logger.info("Logging system initialized")