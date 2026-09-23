"""
Scan Schemas

Defines request and response schemas for security scans.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ------------------------------------------
# Scan Response
# ------------------------------------------

class ScanResponse(BaseModel):
    id: int
    scan_type: str
    status: str
    application_id: int
    results: dict | None = None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ------------------------------------------
# Individual Security Check
# ------------------------------------------

class SecurityCheck(BaseModel):

    check: str

    status: str

    details: str


# ------------------------------------------
# Scan Results
# ------------------------------------------

class ScanResults(BaseModel):

    target: str

    checks: list[SecurityCheck]

    error: str | None = None


# ------------------------------------------
# Complete Scan Execution Response
# ------------------------------------------

class ScanExecutionResponse(BaseModel):

    scan: ScanResponse

    results: ScanResults