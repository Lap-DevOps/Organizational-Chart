import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .. import bcrypt, db
from ..database import Base


class Role(enum.Enum):
    """Enumeration for user roles."""

    admin = "Admin"
    HR = "HR"
    employee = "Employee"
    guest = "Guest"


class User(Base):
    """Model representing a user in the database."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    public_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )

    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.guest)

    password_hash: Mapped[str] = mapped_column(String(256))
    member_since: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    employee_id: Mapped[str] = mapped_column(Integer, nullable=True)

    @property
    def password(self):
        """Unsuccessful attempt to access the password."""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Setting the password hash."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify the entered password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """String representation of the User object."""
        return f"<User(id={self.id!r}, name={self.username!r}, email={self.email!r})>"


class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
