"""
Phishing Analysis Model

Stores phishing email detection results.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
    JSON,
    Float,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PhishingAnalysis(Base):
    """
    Database table for phishing email analysis.
    """

    __tablename__ = "phishing_analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    sender: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    urls: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    classification: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        nullable=False,
    )

    ai_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    rule_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reasons: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
