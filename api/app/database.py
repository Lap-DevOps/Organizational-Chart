"""
Module containing SQLAlchemy base configuration.

This module defines the SQLAlchemy `Base` class with additional configurations,
such as metadata with a custom naming convention.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    This class extends `DeclarativeBase` and includes additional configurations
    like custom metadata with a naming convention.
    """

    __abstract__ = True
    metadata = MetaData(
        naming_convention={
            "all_column_names": lambda constraint, table: "_".join(  # noqa
                [column.name for column in constraint.columns.values()],
            ),
            "ix": "ix__%(table_name)s__%(all_column_names)s",
            "uq": "uq__%(table_name)s__%(all_column_names)s",
            "ck": "ck__%(table_name)s__%(constraint_name)s",
            "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
            "pk": "pk__%(table_name)s",
        },
    )
