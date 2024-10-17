# assessments_app/management/commands/load_assessments.py

import json
from datetime import datetime
from django.core.management.base import BaseCommand
from assessments_app.models import PlaceModel, AssessmentModel


class Command(BaseCommand):
    help = 'Load assessments from a JSON file'

    def handle(self, *args, **kwargs):
        with open('data/assessments.json', 'r') as file:
            data = json.load(file)

        for convocatoria in data['convocatorias']:
            place_name = convocatoria['place']
            place, created = PlaceModel.objects.get_or_create(name=place_name)

            for date_str in convocatoria['dates']:
                # Convertir la fecha al formato YYYY-MM-DD
                date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').date()
                AssessmentModel.objects.create(
                    title=f"Assessment for {place_name}",
                    place=place,
                    date=date
                )

        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded assessments'))
