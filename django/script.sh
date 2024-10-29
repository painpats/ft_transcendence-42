#!/bin/bash

sleep 5

python manage.py makemigrations app
python manage.py migrate

python manage.py collectstatic --noinput

python manage.py initdata

python manage.py makemessages -l en
python manage.py makemessages -l fr
python manage.py makemessages -l es
python manage.py compilemessages

exec gunicorn website.wsgi:application --bind 0.0.0.0:8000
