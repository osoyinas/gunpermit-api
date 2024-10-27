# metrics_app/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from auth_app.mocks import createUserMock, getAuthenticatedClient
from quizzes_app.mocks import createQuizMock
from tracking_app.models import QuizResultModel
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
            QuizResultModel.objects.create(
                quiz=self.quiz,
                user=self.user,
                answers = [random.choice([0, 2]) for _ in range(3)]
            )
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
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
