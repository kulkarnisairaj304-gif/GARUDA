"""
Application Model

Represents an application inside a project.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Application(Base):
    """
    Application database table.
    """

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    application_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    base_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    technology: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    framework: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    environment: Mapped[str] = mapped_column(
        String(50),
        default="Development",
    )

    scan_status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )