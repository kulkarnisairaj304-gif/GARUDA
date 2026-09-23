"""
Scan API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.schemas.scan_schema import ScanExecutionResponse
from app.services.scan_service import ScanService
from app.schemas.scan_schema import ScanResponse


router = APIRouter(
    prefix="/scans",
    tags=["Scans"],
)


# ------------------------------------------
# Start Scan
# ------------------------------------------

@router.post(

    "/applications/{application_id}",
    response_model=ScanExecutionResponse,
    status_code=status.HTTP_201_CREATED,

)
def start_scan(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    scan_service = ScanService(db)

    try:

        return scan_service.start_scan(
            application_id=application_id,
            owner_id=current_user.id,
        )

    except ValueError as e:

        error_message = str(e)

        if "not found" in error_message.lower():

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message,
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_message,
        )
# -------------------------------------------------------
# Get Scan History
# -------------------------------------------------------

@router.get(
    "",
    response_model=list[ScanResponse],
)
def get_scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ScanService(db)

    return service.get_scans(
        current_user.id
    )
# -------------------------------------------------------
# Get Single Scan
# -------------------------------------------------------

@router.get(
    "/{scan_id}",
    response_model=ScanResponse,
)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ScanService(db)

    try:
        return service.get_scan(
            scan_id,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
