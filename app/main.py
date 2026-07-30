"""
Sentinel AI XDR

Main Application

Purpose:
Entry point of the Sentinel AI XDR backend.

Responsibilities:
- Create FastAPI application
- Configure middleware
- Register routes
- Startup and shutdown events

Author:
Sairaj Kulkarni

Project:
Sentinel AI XDR
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import logger
from app.core.database import create_tables
from app.services.database_service import test_database_connection
from app.api.auth_router import router as auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("======================================")
    logger.info(f"Starting {settings.app_name}")
    logger.info(f"Version: {settings.app_version}")

    if not test_database_connection():
        raise RuntimeError("Unable to connect to PostgreSQL.")

    create_tables()

    logger.info("Backend initialized successfully.")
    logger.info("======================================")

    yield

    logger.info("======================================")
    logger.info("Shutting down Sentinel AI XDR...")
    logger.info("======================================")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)
app.include_router(auth_router)
# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint.
    """

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "Running",
        "message": "Welcome to Sentinel AI XDR Backend"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health", tags=["System"])
async def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": settings.app_name
    }