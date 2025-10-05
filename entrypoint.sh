#!/bin/sh

set -e

echo "Waiting for PostgreSQL to be available on the host $POSTGRES_HOST and port $POSTGRES_PORT..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

echo "=================== PostgreSQL is available!"

echo "Waiting for PostgreSQL test to be available on the host $TEST_POSTGRES_HOST and port $TEST_POSTGRES_PORT..."
until pg_isready -h "$TEST_POSTGRES_HOST" -p "$TEST_POSTGRES_PORT" -U "$TEST_POSTGRES_USER"; do
  sleep 1
done

echo "=================== PostgreSQL test is available!"

echo "=================== Running migrations on main database..."
# alembic upgrade head

echo "=================== Launching FastAPI..."
# exec python -m app.main
