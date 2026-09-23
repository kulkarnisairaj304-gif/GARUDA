"""
Phishing Service

Handles phishing email analysis business logic.
"""

from sqlalchemy.orm import Session

from app.models.phishing_analysis import PhishingAnalysis

from app.repositories.phishing_repository import (
    PhishingRepository,
)

from app.schemas.phishing_schema import (
    PhishingAnalysisCreate,
)

from app.services.phishing_engine import PhishingEngine


class PhishingService:

    def __init__(self, db: Session):

        self.repository = PhishingRepository(db)

        self.engine = PhishingEngine()

    # ------------------------------------------
    # Analyze Email
    # ------------------------------------------

    def analyze_email(
        self,
        email_data: PhishingAnalysisCreate,
    ) -> PhishingAnalysis:

        # Run phishing detection
        detection_result = self.engine.analyze(
            sender=email_data.sender,
            subject=email_data.subject,
            body=email_data.body,
            urls=email_data.urls,
        )

        # Create database record
        analysis = PhishingAnalysis(
            sender=email_data.sender,
            subject=email_data.subject,
            body=email_data.body,
            urls=email_data.urls,
            classification=detection_result[
                "classification"
            ],
            risk_score=detection_result[
                "risk_score"
            ],
            confidence=detection_result[
                "confidence"
            ],
            ai_probability=detection_result[
              "ai_probability"
            ],
            rule_score=detection_result[
            "rule_score"
            ],
            reasons=detection_result[
                "reasons"
            ],
        )

        # Save result
        return self.repository.create(
            analysis
        )