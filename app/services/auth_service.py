"""
Authentication Service

Handles user authentication business logic.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository

from app.schemas.user_schema import UserCreate
from app.schemas.token_schema import Token

from app.utils.security import (
    hash_password,
    verify_password,
)

from app.utils.jwt_handler import create_access_token


class AuthService:
    """
    Handles user authentication logic.
    """

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> User:
        """
        Register a new user.
        """

        existing_user = self.user_repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise ValueError("Email is already registered.")

        hashed_password = hash_password(
            user_data.password
        )

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
        )

        return self.user_repository.create_user(
            new_user
        )

    def login_user(
        self,
        email: str,
        password: str,
    ) -> Token:
        """
        Authenticate user and return JWT token.
        """

        print("=" * 60)
        print("LOGIN ATTEMPT")
        print(f"Email: {email}")

        user = self.user_repository.get_by_email(
            email
        )

        print("User Found:", user is not None)

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        print("Stored Email:", user.email)

        password_match = verify_password(
            password,
            user.password_hash,
        )

        print("Password Match:", password_match)
        print("=" * 60)

        if not password_match:
            raise ValueError(
                "Invalid email or password."
            )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )
