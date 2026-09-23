"""
Scan Model

Represents a security scan performed on an application.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    JSON,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from sqlalchemy import JSON


class Scan(Base):

    __tablename__ = "scans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    scan_type: Mapped[str] = mapped_column(
        String(50),
        default="Security Scan",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    results: Mapped[dict | None] = mapped_column(
    JSON,
    nullable=True,
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )