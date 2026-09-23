"""
Phishing Schemas

Defines request and response schemas
for phishing email detection.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ------------------------------------------
# Phishing Analysis Request
# ------------------------------------------

class PhishingAnalysisCreate(BaseModel):

    sender: str

    subject: str

    body: str

    urls: list[str] | None = None


# ------------------------------------------
# Phishing Analysis Response
# ------------------------------------------

class PhishingAnalysisResponse(BaseModel):

    id: int

    sender: str

    subject: str

    body: str

    urls: list[str] | None

    classification: str

    risk_score: int

    confidence: float

    ai_probability: float

    rule_score: int

    reasons: list[str] | None