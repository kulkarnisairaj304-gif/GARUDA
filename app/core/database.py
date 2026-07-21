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
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings
from app.core.logger import logger


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

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass


logger.info("Database configuration initialized.")