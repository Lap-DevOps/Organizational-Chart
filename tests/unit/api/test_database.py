from sqlalchemy import text


def test_alembic_version_table_exists(db):
    """
    Test if the 'alembic_version' table exists in the public schema.
    """
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
        values = [row[0] for row in rows]
        assert any(
            "alembic_version" in row for row in values
        ), "Table 'alembic_version' not found in the public schema."


def test_users_table_exists(db):
    """
    Test if the 'users' table exists in the public schema.
    """
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
        values = [row[0] for row in rows]
        assert any("users" in row for row in values), "Table 'users' not found in the public schema."


def test_table_names_in_db_vs_app(app, db):
    """
    Test to compare table names between the application models and the database.

    :param app: Flask application instance
    :param db: SQLAlchemy database instance
    """
    # Get table names from the SQLAlchemy model
    with app.app_context():
        app_table_names = db.metadata.tables.keys()

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
    assert set(app_table_names) == set(db_table_names + ["alembic_version"])


def test_content_users_table_db_vs_app(app, db):
    """
    Test to compare column names and types between the 'users' table in the application model and the database.

    :param app: Flask application instance
    :param db: SQLAlchemy database instance
    """
    # Get columns from the SQLAlchemy model
    app_columns = db.metadata.tables["users"].columns

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
            column_name, data_type = row
            assert column_name in app_columns, f"Column '{column_name}' not found in the application model."
