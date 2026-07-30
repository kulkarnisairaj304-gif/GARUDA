"""
User Repository

Handles all database operations
related to the User model.
"""

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository for User database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Find a user by email.
        """

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create_user(self, user: User) -> User:
        """
        Save a new user to the database.
        """

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user