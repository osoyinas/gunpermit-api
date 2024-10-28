#bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py load_questions
python3 manage.py load_assessment
python3 manage.py generate_official_tests 10
python3 manage.py createsuperuser