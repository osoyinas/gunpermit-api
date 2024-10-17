import json
from django.core.management.base import BaseCommand
from assessments_app.models import PlaceModel, AssessmentModel

class Command(BaseCommand):
    help = 'Export assessments and places to a JSON file'

    def handle(self, *args, **kwargs):
        data = {"convocatorias": []}

        places = PlaceModel.objects.all()
        for place in places:
            assessments = AssessmentModel.objects.filter(place=place)
            dates = [assessment.date.isoformat() for assessment in assessments]
            data["convocatorias"].append({
                "place": place.name,
                "dates": dates
            })

        with open('data/assessments.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully exported assessments and places to data/assessments.json'))