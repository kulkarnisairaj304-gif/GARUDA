"""
Project Repository

Handles all database operations for Project.
"""

from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate


class ProjectRepository:
    """
    Repository for Project database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------
    # Create
    # ---------------------------------------------------

    def create_project(
        self,
        project: ProjectCreate,
        owner_id: int,
    ) -> Project:

        new_project = Project(
            name=project.name,
            description=project.description,
            owner_id=owner_id,
        )

        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)

        return new_project

    # ---------------------------------------------------
    # Get All Projects By Owner
    # ---------------------------------------------------

    def get_projects_by_owner(
        self,
        owner_id: int,
    ) -> list[Project]:

        return (
            self.db.query(Project)
            .filter(Project.owner_id == owner_id)
            .all()
        )

    # ---------------------------------------------------
    # Get Project By ID
    # ---------------------------------------------------

    def get_project_by_id(
        self,
        project_id: int,
    ) -> Project | None:

        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    # ---------------------------------------------------
    # Update
    # ---------------------------------------------------

    def update_project(
        self,
        project: Project,
        update_data: ProjectUpdate,
    ) -> Project:

        data = update_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():
            setattr(project, key, value)

        self.db.commit()
        self.db.refresh(project)

        return project

    # ---------------------------------------------------
    # Delete
    # ---------------------------------------------------

    def delete_project(
        self,
        project: Project,
    ) -> None:

        self.db.delete(project)
        self.db.commit()