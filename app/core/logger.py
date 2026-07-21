"""
Sentinel AI XDR

Logging Configuration

Purpose:
Configure centralized logging for the entire application.

Responsibilities:
- Console logging
- File logging
- Log formatting
- Application-wide logger

Author:
Sairaj Kulkarni

Project:
Sentinel AI XDR
"""

from pathlib import Path

from loguru import logger

# --------------------------------------------------
# Create Logs Directory
# --------------------------------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "sentinel.log"

# --------------------------------------------------
# Remove Default Logger
# --------------------------------------------------

logger.remove()

# --------------------------------------------------
# Console Logger
# --------------------------------------------------

logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# --------------------------------------------------
# File Logger
# --------------------------------------------------

logger.add(
    LOG_FILE,
    level="DEBUG",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)

logger.info("Logger initialized successfully.")