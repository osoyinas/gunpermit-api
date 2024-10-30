from django.test import TestCase

from auth_app.mocks import createUserMock, getAuthenticatedClient
from quizzes_app.mocks import createQuizMock
from tracking_app.models import QuizResultModel, UserQuestionAttemptModel


class TrackingTests(TestCase):
    def setUp(self):
        self.user = createUserMock()
        self.client = getAuthenticatedClient(self.user)
        self.quiz = createQuizMock()

    def test_make_quiz(self):
        quiz_result = QuizResultModel.objects.create(
            user=self.user,
            quiz=self.quiz
        )
        for question_with_answers in self.quiz.questions.all():
            quiz_result.answers.create(
                question=question_with_answers,
                answer=question_with_answers.correct_answer_index
            )
        quiz_result.save()
        self.assertIsNotNone(quiz_result)

        # Check QuestionAttemptModel creation
        for question_with_answers in quiz_result.answers.all():
            question_attempt = UserQuestionAttemptModel.objects.get(
                user=self.user,
                question=question_with_answers.question
            )
            self.assertIsNotNone(question_attempt)
        self.assertEqual(quiz_result.score, 100)
