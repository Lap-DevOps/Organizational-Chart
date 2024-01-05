#!/bin/bash
set -e

# Run PostgreSQL (standard entrypoint script)
#.docker-entrypoint.sh "$@"

# Check for the presence of Alembic and the configuration file
if command -v alembic &> /dev/null && [ -f "/migrations/alembic.ini" ]; then
  # Check if the database requires migrations
  if alembic -c /migrations/alembic.ini current; then
    # Apply migrations
    alembic -c /migrations/alembic.ini upgrade head
  else
    echo "The database does not require migrations."
  fi
else
  echo "Alembic or the configuration file not found. Skipping migration application."
fi
