import os
import json
from django.core.management.base import BaseCommand
from questions_app.models import QuestionModel, TopicModel

class Command(BaseCommand):
    help = 'Load questions from JSON files into the database'

    def handle(self, *args, **kwargs):
        data_dir = 'data/'
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

        for json_file in json_files:
            file_path = os.path.join(data_dir, json_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                topic_name = data.get('topic', 'Default Topic')
                topic, created = TopicModel.objects.get_or_create(name=topic_name)

                for question_data in data.get('questions', []):
                    question_text = question_data.get('question')
                    options = question_data.get('options', [])
                    answer = question_data.get('answer')
                    answers = [{'answer': option, 'is_true': index == answer} for index, option in enumerate(options)]

                    QuestionModel.objects.create(
                        question=question_text,
                        answers=answers,
                        topic=topic
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded questions from JSON files'))