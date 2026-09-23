"""
Application Repository

Handles database operations for applications.
"""

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.project import Project


class ApplicationRepository:

    """
    Repository for Application database operations.
    """

    def __init__(self, db: Session):

        self.db = db

    # ------------------------------------------
    # Create
    # ------------------------------------------

    def create(
        self,
        application: Application,
    ) -> Application:

        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)

        return application

    # ------------------------------------------
    # Get by ID
    # ------------------------------------------

    def get_by_id(
        self,
        application_id: int,
    ) -> Application | None:

        return (
            self.db.query(Application)
            .filter(Application.id == application_id)
            .first()
        )

    # ------------------------------------------
    # Get All
    # ------------------------------------------

    def get_all(self) -> list[Application]:

        return (
            self.db.query(Application)
            .all()
        )

    # ------------------------------------------
    # Get All by Owner
    # ------------------------------------------

    def get_all_by_owner(
        self,
        owner_id: int,
    ) -> list[Application]:

        return (
            self.db.query(Application)
            .join(
                Project,
                Application.project_id == Project.id,
            )
            .filter(
                Project.owner_id == owner_id
            )
            .all()
        )

    # ------------------------------------------
    # Get by Project
    # ------------------------------------------

    def get_by_project(
        self,
        project_id: int,
    ) -> list[Application]:

        return (
            self.db.query(Application)
            .filter(
                Application.project_id == project_id
            )
            .all()
        )

    # ------------------------------------------
    # Update
    # ------------------------------------------

    def update(
        self,
        application: Application,
    ) -> Application:

        self.db.commit()
        self.db.refresh(application)

        return application

    # ------------------------------------------
    # Delete
    # ------------------------------------------

    def delete(
        self,
        application: Application,
    ):

        self.db.delete(application)
        self.db.commit()