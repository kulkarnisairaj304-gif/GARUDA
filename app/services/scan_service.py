"""
Scan Service

Handles business logic for security scans.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.scan import Scan

from app.repositories.scan_repository import ScanRepository
from app.repositories.application_repository import ApplicationRepository
from app.repositories.project_repository import ProjectRepository

from app.services.scanner_engine import ScannerEngine


class ScanService:

    def __init__(self, db: Session):

        self.scan_repository = ScanRepository(db)

        self.application_repository = ApplicationRepository(db)

        self.project_repository = ProjectRepository(db)

        self.scanner_engine = ScannerEngine()


    # ------------------------------------------
    # Start Scan
    # ------------------------------------------

    def start_scan(
        self,
        application_id: int,
        owner_id: int,
    ):

        # Get application
        application = (
            self.application_repository.get_by_id(
                application_id
            )
        )

        if application is None:
            raise ValueError("Application not found.")

        # Get project
        project = (
            self.project_repository.get_project_by_id(
                application.project_id
            )
        )

        if project is None:
            raise ValueError("Project not found.")

        # Verify ownership
        if project.owner_id != owner_id:
            raise ValueError(
                "Unauthorized access to this application."
            )

        # Create scan record
        scan = Scan(
            scan_type="Security Scan",
            status="Pending",
            application_id=application_id,
            started_at=datetime.utcnow(),
        )

        # Save scan
        scan = self.scan_repository.create(scan)

        # Mark scan as Running
        scan.status = "Running"
        self.scan_repository.update(scan)

        # Run security checks
        scan_results = self.scanner_engine.run_scan(
        application.base_url
        )

        # Save scan results
        scan.results = scan_results

        # Mark scan as Completed
        scan.status = "Completed"
        scan.completed_at = datetime.utcnow()

        self.scan_repository.update(scan)

        return {
        "scan": scan,
        "results": scan_results,
        }
    # ------------------------------------------
    # Get Scan History
    # ------------------------------------------

    def get_scans(
         self,
         owner_id: int,
        ) -> list[Scan]:

        return self.scan_repository.get_by_owner(
        owner_id
        )
    # ------------------------------------------
# Get Single Scan
# ------------------------------------------

    def get_scan(
     self,
        scan_id: int,
        owner_id: int,
    ) -> Scan:

        scan = self.scan_repository.get_by_id(
        scan_id
     )

        if scan is None:
          raise ValueError("Scan not found.")

     # Get application
        application = self.application_repository.get_by_id(
        scan.application_id
    )

        if application is None:
            raise ValueError("Application not found.")

     # Get project
        project = self.project_repository.get_project_by_id(
        application.project_id
    )

        if project is None:
            raise ValueError("Project not found.")

     # Verify ownership
        if project.owner_id != owner_id:
            raise ValueError(
            "Unauthorized access to this scan."
            )

        return scan
