"""
Scan Repository

Handles database operations for security scans.
"""

from app.models.scan import Scan
from app.models.application import Application
from app.models.project import Project


class ScanRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------
    # Create Scan
    # ------------------------------------------

    def create(self, scan: Scan) -> Scan:

        self.db.add(scan)

        self.db.commit()

        self.db.refresh(scan)

        return scan

    # ------------------------------------------
    # Get Scan by ID
    # ------------------------------------------

    def get_by_id(self, scan_id: int) -> Scan | None:

        return (
            self.db.query(Scan)
            .filter(Scan.id == scan_id)
            .first()
        )

    # ------------------------------------------
    # Get All Scans for Application
    # ------------------------------------------

    def get_by_application(
        self,
        application_id: int,
    ) -> list[Scan]:

        return (
            self.db.query(Scan)
            .filter(
                Scan.application_id == application_id
            )
            .all()
        )
    # ------------------------------------------
# Get All Scans for Owner
# ------------------------------------------

    def get_by_owner(
    self,
    owner_id: int,
    ) -> list[Scan]:

         return (
             self.db.query(Scan)
             .join(
              Application,
             Scan.application_id == Application.id,
            )
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
    # Update Scan
    # ------------------------------------------

    def update(self, scan: Scan) -> Scan:

        self.db.commit()

        self.db.refresh(scan)

        return scan
