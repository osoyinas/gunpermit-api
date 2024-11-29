web: mkdir static && python manage.py collectstatic --no-input && python manage.py migrate && gunicorn django_gunpermit.wsgi --bind 0.0.0.0:8080
