"""
Database Service

Purpose:
Provides database-related utility functions.

Current Features:
- Verify PostgreSQL connection

Future Features:
- Database initialization
- Seed default data
- Health monitoring
"""

from sqlalchemy import text

from app.core.database import engine
from app.core.logger import logger


def test_database_connection() -> bool:
    """
    Test whether PostgreSQL is reachable.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info("Database connected successfully.")
        return True

    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False