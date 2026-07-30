"""
Sentinel AI XDR

Database Configuration

Purpose:
Configure SQLAlchemy engine, session factory, and declarative base.

Responsibilities:
- Create database engine
- Manage database sessions
- Provide base model class

Author:
Sairaj Kulkarni

Project:
Sentinel AI XDR
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logger import logger
from app.models.base import Base

# Import models so SQLAlchemy knows they exist
from app.models.user import User


# --------------------------------------------------
# Database Engine
# --------------------------------------------------

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)


# --------------------------------------------------
# Session Factory
# --------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# --------------------------------------------------
# Base Model
# --------------------------------------------------
logger.info("Database configuration initialized.")


def create_tables() -> None:
    """
    Create all database tables.
    """

    logger.info("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database tables created successfully.")

def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    