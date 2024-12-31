# metrics_app/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from auth_app.mocks import createUserMock, getAuthenticatedClient
from quizzes_app.mocks import createQuizMock
from tracking_app.models import QuestionWithAnswerModel, QuizResultModel, UserQuestionAttemptModel
from questions_app.models import TopicModel, QuestionModel
import random
import json


class ListUserResultsTests(APITestCase):
    def setUp(self):
        self.user = createUserMock(
            email='staff@gmail.com', username='staff')
        self.client = getAuthenticatedClient(self.user)
        self.url = reverse('results')

        self.quiz = createQuizMock()
        # Create some QuizResultModel instances
        for i in range(15):
            quiz_result = QuizResultModel.objects.create(
                quiz=self.quiz,
                user=self.user,
            )
            for question in self.quiz.questions.all():
                question_with_answer = QuestionWithAnswerModel.objects.create(
                    question=question,
                    answer=random.randint(0, len(question.answers) - 1)
                )
                quiz_result.answers.add(question_with_answer)

    def test_list_user_results_default_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Default page size is 10
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_list_user_results_custom_pagination(self):
        response = self.client.get(self.url, {'size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Custom page size is 5
        self.assertEqual(len(response.data['results']), 5)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_list_user_results_invalid_pagination(self):
        response = self.client.get(self.url, {'size': 120})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Page size should default to 10
        self.assertEqual(len(response.data['results']), 15)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)


class UserQuestionAttemptsViewTests(APITestCase):
    def setUp(self):
        self.user = createUserMock(email='user@gmail.com', username='user')
        self.client = getAuthenticatedClient(self.user)
        self.url = reverse('user_question_attempts')

        self.topic1 = TopicModel.objects.create(title='Math', description='Math questions')
        self.topic2 = TopicModel.objects.create(title='Science', description='Science questions')

        self.question1 = QuestionModel.objects.create(question='What is 2+2?', topic=self.topic1, answers=[
            {'answer': '4', 'is_true': True},
            {'answer': '3', 'is_true': False},
            {'answer': '5', 'is_true': False}
        ])
        self.question2 = QuestionModel.objects.create(question='What is the chemical symbol for water?', topic=self.topic2, answers=[
            {'answer': 'H2O', 'is_true': True},
            {'answer': 'O2', 'is_true': False},
            {'answer': 'CO2', 'is_true': False}
        ])

        UserQuestionAttemptModel.objects.create(user=self.user, question=self.question1, is_correct=True)
        UserQuestionAttemptModel.objects.create(user=self.user, question=self.question2, is_correct=False)

    def test_user_question_attempts_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answered'], 2)
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['topics']['Math']['answered'], 1)
        self.assertEqual(response.data['topics']['Math']['total'], 1)
        self.assertEqual(response.data['topics']['Math']['correct'], 1)
        self.assertEqual(response.data['topics']['Math']['incorrect'], 0)
        self.assertEqual(response.data['topics']['Science']['answered'], 1)
        self.assertEqual(response.data['topics']['Science']['total'], 1)
        self.assertEqual(response.data['topics']['Science']['correct'], 0)
        self.assertEqual(response.data['topics']['Science']['incorrect'], 1)
