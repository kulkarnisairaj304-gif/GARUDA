"""
Project Router

API endpoints for Project management.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)

from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# ---------------------------------------------------
# Create Project
# ---------------------------------------------------

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project_service = ProjectService(db)

    return project_service.create_project(
        project=project,
        current_user=current_user,
    )


# ---------------------------------------------------
# Get All Projects
# ---------------------------------------------------

@router.get(
    "",
    response_model=list[ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project_service = ProjectService(db)

    return project_service.get_projects(
        current_user=current_user,
    )


# ---------------------------------------------------
# Get Project By ID
# ---------------------------------------------------

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project_service = ProjectService(db)

    return project_service.get_project(
        project_id=project_id,
        current_user=current_user,
    )


# ---------------------------------------------------
# Update Project
# ---------------------------------------------------

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    update_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project_service = ProjectService(db)

    return project_service.update_project(
        project_id=project_id,
        update_data=update_data,
        current_user=current_user,
    )


# ---------------------------------------------------
# Delete Project
# ---------------------------------------------------

@router.delete(
    "/{project_id}",
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    project_service = ProjectService(db)

    return project_service.delete_project(
        project_id=project_id,
        current_user=current_user,
    )