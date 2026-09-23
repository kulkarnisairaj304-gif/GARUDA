"""
Project Schemas

Pydantic schemas for Project operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """
    Schema for creating a project.
    """

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class ProjectUpdate(BaseModel):
    """
    Schema for updating a project.
    """

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class ProjectResponse(BaseModel):
    """
    Schema returned by the API.
    """

    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )