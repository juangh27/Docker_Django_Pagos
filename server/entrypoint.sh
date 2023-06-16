#!/bin/sh
# Run database migrations

# revisar que el archivo sh sea LF en vez de CRLF

python manage.py makemigrations
python manage.py migrate

# Collect static files
# python manage.py collectstatic --noinput

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

python manage.py runserver 0.0.0.0:8000