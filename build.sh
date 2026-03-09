#!/usr/bin/env bash
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py shell < create_superuser.py