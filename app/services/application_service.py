"""
Application Service

Handles business logic for applications.
"""

from sqlalchemy.orm import Session

from app.models.application import Application
from app.repositories.application_repository import ApplicationRepository
from app.repositories.project_repository import ProjectRepository

from app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationUpdate,
)


class ApplicationService:
    """
    Handles application business logic.
    """

    def __init__(self, db: Session):
     self.application_repository = ApplicationRepository(db)
     self.project_repository = ProjectRepository(db)
    # ---------------------------------------------------
    # Create
    # ---------------------------------------------------

    def create_application(
    self,
    application_data: ApplicationCreate,
    owner_id: int,
) -> Application:

        project = self.project_repository.get_project_by_id(
        application_data.project_id
    )

        if project is None:
         raise ValueError("Project not found.")

        if project.owner_id != owner_id:
            raise ValueError("Unauthorized project.")

        application = Application(
            name=application_data.name,
            description=application_data.description,
            application_type=application_data.application_type,
            base_url=application_data.base_url,
            technology=application_data.technology,
            framework=application_data.framework,
            environment=application_data.environment,
            project_id=application_data.project_id,
)


        return self.application_repository.create(application)

    # ---------------------------------------------------
    # Get All
    # ---------------------------------------------------

    def get_all(
    self,
    owner_id: int,
):

     return self.application_repository.get_all_by_owner(
        owner_id
    )

    # ---------------------------------------------------
    # Get One
    # ---------------------------------------------------

    def get_application(
        self,
        application_id: int,
    ):

        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            raise ValueError("Application not found.")

        return application
    # ---------------------------------------------------
    # Scan Application
    # ---------------------------------------------------

    def scan_application(
        self,
        application_id: int,
        owner_id: int,
    ):

        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            raise ValueError("Application not found.")

        project = self.project_repository.get_project_by_id(
            application.project_id
        )

        if project is None:
            raise ValueError("Project not found.")

        if project.owner_id != owner_id:
            raise ValueError("Unauthorized application.")

        # Change scan status
        application.scan_status = "Scanning"

        self.application_repository.update(application)

        # For now, simulate scan completion
        application.scan_status = "Completed"

        return self.application_repository.update(application)
    # ---------------------------------------------------
    # Update
    # ---------------------------------------------------

    def update_application(
        self,
        application_id: int,
        application_data: ApplicationUpdate,
    ):

        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            raise ValueError("Application not found.")

        application.name = application_data.name
        application.description = application_data.description

        return self.application_repository.update(application)

    # ---------------------------------------------------
    # Delete
    # ---------------------------------------------------

    def delete_application(
        self,
        application_id: int,
    ):

        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            raise ValueError("Application not found.")

        self.application_repository.delete(application)

        return {
            "message": "Application deleted successfully."
        }
