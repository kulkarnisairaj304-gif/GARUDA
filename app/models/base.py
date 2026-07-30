"""
Base Model

Purpose:
Defines the SQLAlchemy Declarative Base class.

Every database model in Sentinel AI XDR
inherits from this class.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass