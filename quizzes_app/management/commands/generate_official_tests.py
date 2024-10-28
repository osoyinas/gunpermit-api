import random
import os
import json
from django.core.management.base import BaseCommand
from questions_app.models import QuestionModel
from quizzes_app.models import QuizCategoryModel, QuizModel, QuizQuestionModel


class Command(BaseCommand):
    help = 'Generate quizzes based on the structure defined in quizzes_schema.json'

    def add_arguments(self, parser):
        parser.add_argument('num_tests', type=int,
                            help='The number of tests to generate')

    def handle(self, *args, **kwargs):
        num_tests = kwargs['num_tests']
        schema_file_path = os.path.join('data', 'quizzes_schema.json')

        # Load the schema
        with open(schema_file_path, 'r', encoding='utf-8') as schema_file:
            schema_data = json.load(schema_file)

        oficial_category, created = QuizCategoryModel.objects.get_or_create(tag='oficial',
                                                                            defaults={
                                                                                'title': 'Oficial',
                                                                                'description': 'Quizzes oficiales',
                                                                                'tag': 'oficial'}
                                                                            )
        for test_num in range(num_tests):
            quiz = QuizModel.objects.create(
                title=f'Test {test_num + 1}', number=test_num + 1, category=oficial_category)
            order = 0

            for item in schema_data:
                topic_id = item['topic']
                num_questions = item['questions']

                # Get questions for the topic
                questions = list(
                    QuestionModel.objects.filter(topic_id=topic_id))
                if len(questions) < num_questions:
                    self.stdout.write(self.style.ERROR(
                        f'Not enough questions for topic {topic_id}'))
                    continue

                selected_questions = random.sample(questions, num_questions)

                for question in selected_questions:
                    QuizQuestionModel.objects.create(
                        quiz=quiz, question=question, order=order)
                    order += 1

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created quiz {quiz.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {num_tests} quizzes'))
