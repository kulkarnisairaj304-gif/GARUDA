"""
Application Schemas

Pydantic models for Application APIs.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# --------------------------------------------------
# Create Application
# --------------------------------------------------

class ApplicationCreate(BaseModel):
    """
    Schema for creating an application.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: Optional[str] = None

    application_type: str

    base_url: str

    technology: Optional[str] = None

    framework: Optional[str] = None

    environment: Optional[str] = "Development"

    project_id: int


# --------------------------------------------------
# Update Application
# --------------------------------------------------

class ApplicationUpdate(BaseModel):
    """
    Schema for updating an application.
    """

    name: Optional[str] = None

    description: Optional[str] = None

    application_type: Optional[str] = None

    base_url: Optional[str] = None

    technology: Optional[str] = None

    framework: Optional[str] = None

    environment: Optional[str] = None


# --------------------------------------------------
# Response Schema
# --------------------------------------------------

class ApplicationResponse(BaseModel):
    """
    Schema returned to the client.
    """

    id: int

    name: str

    description: Optional[str]

    application_type: str

    base_url: str

    technology: Optional[str]

    framework: Optional[str]

    environment: str

    scan_status: str

    project_id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )