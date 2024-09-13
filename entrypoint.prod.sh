#!/bin/sh

if [ "$POSTGRES_DATABASE" = "postgres" ]
then
    echo "Postgres еще не запущен..."

    # Проверяем доступность хоста и порта
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Postgres запущен"
fi

python manage.py makemigrations tender --no-input

python manage.py migrate --fake-initial

python manage.py makemigrations tender --no-input

python manage.py migrate tender --no-input

python manage.py runserver 0.0.0.0:8000

exec "$@"