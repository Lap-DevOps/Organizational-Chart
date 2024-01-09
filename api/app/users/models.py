import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .. import bcrypt
from ..database import Base

# from ...app import bcrypt


class Role(enum.Enum):
    admin = "Admin"
    HR = "HR"
    employee = "Employee"
    guest = "Guest"


class User(Base):
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
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, index=True
    )
    role: Mapped[Role] = mapped_column(nullable=False, default=Role.guest)

    password_hash: Mapped[str] = mapped_column(String(256))
    member_since: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    employee_id: Mapped[str] = mapped_column(Integer, nullable=True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        ...
        return f"<User(id={self.id!r}, name={self.username!r}, email={self.email!r})>"
