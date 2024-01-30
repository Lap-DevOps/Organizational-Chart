import pytest
from flask.testing import FlaskClient

from app.users.models import Role
from app.users.schemas import UserDto


def test_user_schema_username():
    model = UserDto.user_schema
    assert model["username"].required == True
    assert model["username"].min_length == 3
    assert model["username"].max_length == 120
    assert model["username"].description == "User name"
    assert model["username"].example == "username"
    assert model["username"].pattern == r"^[a-zA-Z0-9_]+$"


def test_user_schema_email():
    model = UserDto.user_schema
    assert model["email"].required == True
    assert model["email"].min_length == 6
    assert model["email"].max_length == 120
    assert model["email"].description == "User email address"
    assert model["email"].example == "user@test.com"
    # assert model["email"].pattern == r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    assert model["email"].pattern == r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$"


def test_user_schema_role():
    model = UserDto.user_schema
    assert model["role"].required == True
    assert model["role"].description == "User role"
    assert model["role"].enum == [role.name for role in Role]
    assert model["role"].attribute == "role"
    assert model["role"].default == "guest"


def test_user_schema_employee_id():
    model = UserDto.user_schema
    assert model["employee_id"].required == True
    assert model["employee_id"].description == "User employee id"
    assert model["employee_id"].example == "1"
    assert model["employee_id"].default == 0


def test_user_schema_creation(client: FlaskClient) -> None:
    """
    Function to test the creation of a user schema using the provided client.
    """
    user_data = {
        "username": "jon_doe",
        "email": "john.doe@example.com",
        "role": "guest",
        "employee_id": 123,
    }
    response = client.post("api/v1/user/", json=user_data)
    assert response.status_code == 200


# Define parameterized test cases for invalid usernames and their expected errors
@pytest.mark.parametrize(
    "invalid_username",
    [
        (""),
        (" "),
        ("  "),
        ("1234@"),
        ("@#$111"),
        ("1234@#$"),
        ("Jon Doe"),
        ("jon doe"),
        ("jon-doe"),
        ("jon=doe"),
        ("john.doe@example.com"),
    ],
)
def test_invalid_username_creation(client: FlaskClient, invalid_username: str) -> None:
    """
    Parameterized test to check error handling during user schema creation with invalid username.
    """
    invalid_user_data = {
        "username": invalid_username,
        "email": "john.doe@example.com",
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=invalid_user_data)

    assert response.status_code == 400
    assert b"Input payload validation failed" in response.json["message"].encode()
    assert "does not match '^[a-zA-Z0-9_]+$" in response.data.decode()


def test_required_username_creation(client: FlaskClient) -> None:
    """
    Test to check that 'username' is required during user schema creation.
    """
    user_data = {
        "email": "john.doe@example.com",
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=user_data)

    assert response.status_code == 400
    assert "'username' is a required property" in str(response.json["errors"])
    assert b"Input payload validation failed" in response.json["message"].encode()


def test_invalid_username_min_length(client: FlaskClient) -> None:
    """
    Test to check that 'username' length is between 3 and 120 characters during user schema creation.
    """
    user_data = {
        "username": "aq",
        "email": "john.doe@example.com",
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=user_data)

    assert response.status_code == 400
    assert "is too short" in str(response.json["errors"])
    assert b"Input payload validation failed" in response.json["message"].encode()


def test_invalid_username_max_length(client: FlaskClient) -> None:
    """
    Test to check that 'username' length is between 3 and 120 characters during user schema creation.
    """
    user_data = {
        "username": "a" * 121,
        "email": "john.doe@example.com",
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=user_data)

    assert response.status_code == 400
    assert "is too long" in str(response.json["errors"])
    assert b"Input payload validation failed" in response.json["message"].encode()


@pytest.mark.parametrize(
    "invalid_email",
    [
        (""),
        (" "),
        ("  "),
        ("1234@"),
        ("@#$111"),
        ("1234@#$"),
        ("Jon Doe"),
        ("jon doe"),
        ("jon-doe"),
        ("jon=doe"),
        ("john.doe@example_com"),
        ("john..doe@example..com"),
        ("invalid.email@com"),
        ("@invalid.com"),
        ("invalid@.com"),
        ("jon.dou.ivanov@example_com"),
    ],
)
def test_invalid_email_creation(client: FlaskClient, invalid_email: str) -> None:
    """
    Parameterized test to check error handling during user schema creation with invalid email.
    """
    invalid_user_data = {
        "username": "valid_username",
        "email": invalid_email,
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=invalid_user_data)

    assert response.status_code == 400
    assert b"Input payload validation failed" in response.json["message"].encode()
    assert "does not match" in response.data.decode()


def test_invalid_email_min_lenght(client: FlaskClient) -> None:
    """
    Test to check that 'email' length is between 6 and 120 characters during user schema creation.
    """
    user_data = {
        "username": "valid_username",
        "email": "a@a.c",
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=user_data)

    assert response.status_code == 400
    assert "is too short" in str(response.json["errors"])
    assert b"Input payload validation failed" in response.json["message"].encode()


def test_invalid_email_max_lenght(client: FlaskClient) -> None:
    """
    Test to check that 'email' length is between 6 and 120 characters during user schema creation.
    """
    user_data = {
        "username": "valid_username",
        "email": "a" * 120 + "@example.com",
        "role": "guest",
        "employee_id": 123,
    }

    response = client.post("/api/v1/user/", json=user_data)

    assert response.status_code == 400
    assert "is too long" in str(response.json["errors"])
    assert b"Input payload validation failed" in response.json["message"].encode()
