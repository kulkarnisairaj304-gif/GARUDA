"""
Sentinel AI XDR

Dependency Management

Purpose:
Provide reusable FastAPI dependencies.

Responsibilities:
- Database session lifecycle
- Shared dependencies

Author:
Sairaj Kulkarni

Project:
Sentinel AI XDR
"""

from collections.abc import Generator

from app.core.database import SessionLocal


def get_db() -> Generator:
    """
    Create a database session for each request.

    The session is automatically closed after the
    request has finished.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()