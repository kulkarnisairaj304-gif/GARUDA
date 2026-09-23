"""
Project Service

Contains business logic for Project operations.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.project_repository import ProjectRepository

from app.schemas.project_schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)


class ProjectService:
    """
    Service layer for Project operations.
    """

    def __init__(self, db: Session):
        self.repository = ProjectRepository(db)

    # ---------------------------------------------------
    # Create Project
    # ---------------------------------------------------

    def create_project(
        self,
        project: ProjectCreate,
        current_user: User,
    ) -> ProjectResponse:

        new_project = self.repository.create_project(
            project=project,
            owner_id=current_user.id,
        )

        return ProjectResponse.model_validate(
            new_project
        )

    # ---------------------------------------------------
    # Get All Projects
    # ---------------------------------------------------

    def get_projects(
        self,
        current_user: User,
    ) -> list[ProjectResponse]:

        projects = self.repository.get_projects_by_owner(
            owner_id=current_user.id,
        )

        return [
            ProjectResponse.model_validate(project)
            for project in projects
        ]

    # ---------------------------------------------------
    # Get Project By ID
    # ---------------------------------------------------

    def get_project(
        self,
        project_id: int,
        current_user: User,
    ) -> ProjectResponse:

        project = self.repository.get_project_by_id(
            project_id
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        return ProjectResponse.model_validate(project)

    # ---------------------------------------------------
    # Update Project
    # ---------------------------------------------------

    def update_project(
        self,
        project_id: int,
        update_data: ProjectUpdate,
        current_user: User,
    ) -> ProjectResponse:

        project = self.repository.get_project_by_id(
            project_id
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        updated_project = self.repository.update_project(
            project,
            update_data,
        )

        return ProjectResponse.model_validate(
            updated_project
        )

    # ---------------------------------------------------
    # Delete Project
    # ---------------------------------------------------

    def delete_project(
        self,
        project_id: int,
        current_user: User,
    ):

        project = self.repository.get_project_by_id(
            project_id
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found.",
            )

        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        self.repository.delete_project(
            project
        )

        return {
            "message": "Project deleted successfully."
        }