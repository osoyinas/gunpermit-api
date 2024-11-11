#bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py load_questions
python manage.py load_assessments
python manage.py generate_official_tests 10
python manage.py generate_tests_by_topics
python manage.py createsuperuser