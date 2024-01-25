""" Module containing user-related Marshmallow schemas."""

from marshmallow import fields, Schema, validate


class UserRegistrationSchema(Schema):
    """
    Schema for user registration.

    Attributes:
        username: User's username.
        email: User's email address.
        password: User's password.

    Raises:
        ValidationError: If validation fails.
    """

    username: str = fields.String(
        required=True,
        validate=[
            validate.Length(min=5, max=120, error="Username must be between 5 and 120 characters."),
            validate.Regexp(r"^[a-zA-Z0-9_]+$", error="Username can only contain letters, numbers, and underscores"),
        ],
        error_messages={
            "required": "Username is required.",
            "validator_failed": "Custom message for validator failure.",
        },
    )
    email: str = fields.Email(
        required=True,
        validate=[
            validate.Email(error="Not a valid email address."),
            validate.Length(min=5, max=120, error="Email must be between 5 and 120 characters."),
        ],
        error_messages={
            "required": "Email is required.",
            "validator_failed": "Custom message for validator failure.",
        },
    )
    password: str = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=256, error="Password must be between 8 and 256 characters."),
            validate.Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                error="Password must contain at least one uppercase letter, one lowercase letter, and one number",
            ),
        ],
        error_messages={
            "required": "Password is required.",
            "validator_failed": "Custom message for validator failure.",
        },
    )
