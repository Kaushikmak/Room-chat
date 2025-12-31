#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static asset files (needed for Admin panel CSS)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate