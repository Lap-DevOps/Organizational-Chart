"""
Module Description.

This module defines the User model and related functionality for managing users in the database.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Literal

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.extensions import bcrypt


class Role(Enum):
    """Enumeration for user roles."""

    admin: Literal["Admin"] = "Admin"
    HR: Literal["HR"] = "HR"
    employee: Literal["Employee"] = "Employee"
    guest: Literal["Guest"] = "Guest"


class User(Base):
    """Model representing a user in the database."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    public_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4),
    )

    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.guest)

    password_hash: Mapped[str] = mapped_column(String(256))
    member_since: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    employee_id: Mapped[str] = mapped_column(Integer, nullable=True)

    @property
    def password(self) -> None:
        """
        Getter method for the password attribute.

        Raises:
            AttributeError: If an attempt is made to access the password attribute.
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        """
        Setter method for the password attribute.

        Args:
            password (str): The password to set.

        Description:
        This method sets the password hash by generating a password hash using `bcrypt`
        and decoding it to UTF-8.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password) -> bool:
        """
        Verify the entered password.

        Args:
            password (str): The password to be verified.

        Returns:
            bool: True if the password matches the stored password hash, False otherwise.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Return a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return f"<User(id={self.id!r}, name={self.username!r}, email={self.email!r})>"
