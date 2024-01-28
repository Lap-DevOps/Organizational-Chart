""" Module containing user-related Marshmallow schemas."""
from flask_restx import Namespace, fields

from app.users.models import Role


class UserDto:
    """User data transfer object."""

    api = Namespace("user", description="User related operations")

    user_schema = api.model(
        "user_schema",
        {
            "username": fields.String(
                required=True,
                min_length=3,
                max_length=120,
                description="User name",
                example="username",
                pattern=r"^[a-zA-Z0-9_]+$",
            ),
            "email": fields.String(
                required=True,
                min_length=6,
                max_length=120,
                description="User email address",
                example="user@test.com",
                pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            ),
            "role": fields.String(
                required=True,
                description="User role",
                example="guest",
                enum=[role.name for role in Role],
                attribute="role",
                default="guest",
            ),
            "employee_id": fields.Integer(required=True, description="User employee id", example="1", default=0),
        },
    )

