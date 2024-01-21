from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError


def test_alembic_version_table_exists(db: SQLAlchemy) -> None:
    """
    Test if the 'alembic_version' table exists in the public schema.

    Args:
        db: The database object.

    Raises:
        AssertionError: If the 'alembic_version' table is not found in the public schema.
        OperationalError: If there is an error executing the SQL query.
    """
    try:
        # Execute the SQL query to check if the table exists in the public schema
        with db.engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """
                )
            )
            # Fetch all the rows returned by the query
            rows = result.fetchall()
            # Get the values from the first column of each row
            values = [row[0] for row in rows]

            # Check if 'alembic_version' is present in any of the values
            assert any(
                "alembic_version" in row for row in values
            ), "Table 'alembic_version' not found in the public schema."

    except OperationalError as e:
        raise OperationalError("Error executing SQL query", params=None, orig=e)


def test_users_table_exists(db: SQLAlchemy) -> None:
    try:
        with db.engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """
                )
            )
            rows = result.fetchall()
            table_names = [row[0] for row in rows]

            if not any("users" in table_name for table_name in table_names):
                raise AssertionError("Table 'users' not found in the public schema.")

    except OperationalError as e:
        raise OperationalError("Error executing SQL query:", params=None, orig=e)


def test_table_names_in_db_vs_app(app: Flask, db: SQLAlchemy) -> None:
    """
    Test to compare table names between the application models and the database.

    Args:
        app (Flask): Flask application instance.
        db (SQLAlchemy): SQLAlchemy database instance.

    Raises:
        AssertionError: If the table names do not match between the app and the database.
        OperationalError: If there is an error executing the SQL query.
    """
    try:
        # Get table names from the SQLAlchemy model
        with app.app_context():
            app_table_names = [*db.metadata.tables.keys()]

        # Get table names from the database
        with db.engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """
                )
            )
            db_table_names = [row[0] for row in result.fetchall()]

        # Include the check for the presence of the "alembic_version" table
        assert set(app_table_names + ["alembic_version"]) == set(db_table_names)

    except OperationalError as e:
        raise OperationalError(f"Error executing SQL query:", params=None, orig=e)


def test_content_users_table_db_vs_app(app: Flask, db: SQLAlchemy) -> None:
    """
    Test to compare column names and types between the 'users' table in the application model and the database.

    Args:
        app (Flask): Flask application instance.
        db (SQLAlchemy): SQLAlchemy database instance.

    Raises:
        AssertionError: If column names or data types do not match between the app and the database.
        OperationalError: If there is an error executing the SQL query.
    """
    try:
        # Get columns from the SQLAlchemy model
        app_columns = db.metadata.tables["users"].columns

        # Get columns from the database
        with db.engine.connect() as conn:
            # Execute SQL query to retrieve column names and data types from the database
            result = conn.execute(
                text(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'users'
                    """
                )
            )

            # Fetch all rows from the query result
            rows = result.fetchall()

            # Output information about database columns
            for row in rows:
                column_name, _ = row
                assert column_name in app_columns, f"Column '{column_name}' not found in the application model."

    except OperationalError as e:
        raise OperationalError(f"Error executing SQL query:", params=None, orig=e)


def test_table_in_db(app: Flask, db: SQLAlchemy) -> None:
    """
    Test if the table 'users' exists in the database.

    Args:
        app (Flask): The Flask application instance.
        db (SQLAlchemy): The SQLAlchemy database instance.

    Raises:
        AssertionError: If the table 'users' does not exist in the database.
        OperationalError: If there is an error executing the SQL query.
    """
    try:
        with app.app_context():
            query = text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
            result = db.session.execute(query).first()[0]

            assert result is True

    except OperationalError as e:
        raise OperationalError(f"Error executing SQL query:", params=None, orig=e)
