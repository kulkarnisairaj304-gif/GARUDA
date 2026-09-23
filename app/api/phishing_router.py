"""
Phishing API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.phishing_schema import (
    PhishingAnalysisCreate,
    PhishingAnalysisResponse,
)

from app.services.phishing_service import PhishingService


router = APIRouter(
    prefix="/phishing",
    tags=["Phishing Detection"],
)


# -------------------------------------------------------
# Analyze Email
# -------------------------------------------------------

@router.post(
    "/analyze",
    response_model=PhishingAnalysisResponse,
    status_code=201,
)
def analyze_email(
    email_data: PhishingAnalysisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PhishingService(db)

    try:

        return service.analyze_email(
            email_data
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )