#!/bin/sh

echo "Применение миграций"
alembic upgrade head

exec "$@"