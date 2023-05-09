#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Make database migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
