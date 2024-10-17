# assessments_app/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from assessments_app.models import PlaceModel, AssessmentModel
from assessments_app.serializers import AssessmentSerializer
from datetime import datetime, timedelta

from auth_app.mocks import createUserStaffMock, getAuthenticatedClient


class AssessmentTests(APITestCase):

    def setUp(self):
        self.place = PlaceModel.objects.create(
            name="Test Place", province="Test Province")
        self.assessment1 = AssessmentModel.objects.create(
            title="Assessment 1",
            place=self.place,
            date=datetime.now().date() + timedelta(days=1)
        )
        self.assessment2 = AssessmentModel.objects.create(
            title="Assessment 2",
            place=self.place,
            date=datetime.now().date() + timedelta(days=2)
        )
        self.assessment3 = AssessmentModel.objects.create(
            title="Assessment 3",
            place=self.place,
            date=datetime.now().date() - timedelta(days=1)
        )
        self.staff_user = createUserStaffMock(
            email='staff@gmail.com', username='staff')
        self.client = getAuthenticatedClient(self.staff_user)


    def test_list_create_assessment(self):
        url = reverse('list_create_assessment')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        data = {
            "title": "New Assessment",
            "place": self.place.id,
            "date": (datetime.now().date() + timedelta(days=3)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AssessmentModel.objects.count(), 4)

    def test_retrieve_update_destroy_assessment(self):
        url = reverse('retrieve_update_destroy_assessment',
                      args=[self.assessment1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.assessment1.title)

        data = {
            "title": "Updated Assessment",
            "place": self.place.id,
            "date": self.assessment1.date.isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assessment1.refresh_from_db()
        self.assertEqual(self.assessment1.title, "Updated Assessment")

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AssessmentModel.objects.count(), 2)

    def test_next_assessment_by_place(self):
        url = reverse('next_assessment', args=[self.place.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.assessment1.title)
        print(response.data)
