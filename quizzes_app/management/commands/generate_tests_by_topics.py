import random
from django.core.management.base import BaseCommand
from questions_app.models import QuestionModel, TopicModel
from quizzes_app.models import QuizCategoryModel, QuizModel, QuizQuestionModel


class Command(BaseCommand):
    help = 'Generate quizzes for each topic and tag them as "by-topic"'

    def handle(self, *args, **kwargs):
        num_questions = 10  # Número fijo de preguntas por quiz
        by_topic_category, _ = QuizCategoryModel.objects.get_or_create(
            tag='by-topic', defaults={'title': 'Exámenes de un tema', 'description': 'Exámenes dividos por tema'}
        )

        topics = TopicModel.objects.all()
        topic_number = 1
        for topic in topics:
            questions = list(QuestionModel.objects.filter(topic=topic))
            if len(questions) < num_questions:
                self.stdout.write(self.style.ERROR(
                    f'Not enough questions for topic {topic.title}'))
                continue

            quiz = QuizModel.objects.create(
                title=f'{topic.title} Quiz', number=topic_number, category=by_topic_category)
            topic_number += 1
            for order, question in enumerate(questions):
                QuizQuestionModel.objects.create(
                    quiz=quiz, question=question, order=order)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created quiz for topic {topic.title}'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully created quizzes for all topics'))
