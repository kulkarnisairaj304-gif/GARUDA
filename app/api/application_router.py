"""
Application API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
)

from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


# -------------------------------------------------------
# Create
# -------------------------------------------------------

@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=201,
)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = ApplicationService(db)

    try:
        return service.create_application(
            application_data,
            current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# -------------------------------------------------------
# Get All
# -------------------------------------------------------

@router.get(
    "",
    response_model=list[ApplicationResponse],
)
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = ApplicationService(db)

    return service.get_all(
    current_user.id
)


# -------------------------------------------------------
# Get One
# -------------------------------------------------------

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = ApplicationService(db)

    try:
        return service.get_application(application_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# -------------------------------------------------------
# Update
# -------------------------------------------------------

@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = ApplicationService(db)

    try:
        return service.update_application(
            application_id,
            application_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# -------------------------------------------------------
# Delete
# -------------------------------------------------------

@router.delete(
    "/{application_id}",
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = ApplicationService(db)

    try:
        return service.delete_application(application_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )