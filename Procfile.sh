#!/bin/bash
service ssh start
python create_env_file_from_json.py --environment-name "$ENVIRONMENT_NAME" --output-file-name=".env"
python manage.py compilemessages
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn -b 0.0.0.0:8000 -c gunicorn.conf.py dm_apps.wsgi:application