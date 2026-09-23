"""
Phishing Repository

Handles database operations for phishing analysis.
"""

from sqlalchemy.orm import Session

from app.models.phishing_analysis import PhishingAnalysis


class PhishingRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------
    # Create Analysis
    # ------------------------------------------

    def create(
        self,
        analysis: PhishingAnalysis,
    ) -> PhishingAnalysis:

        self.db.add(analysis)

        self.db.commit()

        self.db.refresh(analysis)

        return analysis

    # ------------------------------------------
    # Get Analysis by ID
    # ------------------------------------------

    def get_by_id(
        self,
        analysis_id: int,
    ) -> PhishingAnalysis | None:

        return (
            self.db.query(PhishingAnalysis)
            .filter(
                PhishingAnalysis.id == analysis_id
            )
            .first()
        )

    # ------------------------------------------
    # Get All Analyses
    # ------------------------------------------

    def get_all(self) -> list[PhishingAnalysis]:

        return (
            self.db.query(PhishingAnalysis)
            .order_by(
                PhishingAnalysis.created_at.desc()
            )
            .all()
        )