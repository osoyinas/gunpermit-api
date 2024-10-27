from django.db import models
from django.forms import ValidationError

from auth_app.models import CustomUser
from questions_app.models import QuestionModel
from quizzes_app.models import QuizModel

# Create your models here.


class QuizResultModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quiz.title} - {self.score}'

    def clean_answers(self):
        if not isinstance(self.answers, list):
            raise ValidationError("El campo 'answers' debe ser una lista.")

        if len(self.answers) != self.quiz.questions.count():
            raise ValidationError(
                f"El campo 'answers' debe tener exactamente {self.quiz.questions.count()} elementos.")

        for answer in self.answers:
            if not isinstance(answer, int):
                raise ValidationError(
                    "Cada elemento en 'answers' debe ser un entero.")

    @property
    def correct_answers(self):
        correct_answers = 0
        for index, question in enumerate(self.quiz.questions.all()):
            if index == question.correct_answer_index:
                correct_answers += 1
        return correct_answers

    @property
    def score(self):
        total_questions = self.quiz.questions.count()
        if total_questions == 0:
            return 0
        return (self.correct_answers / total_questions) * 100

    @property
    def score_str(self):
        return f'{self.correct_answers}/{self.quiz.questions.count()}'

    @property
    def passed(self):
        return self.score >= 80  # 16/20 80% passing grade


class UserQuestionAttemptModel(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="question_attempts")
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="user_attempts")
    answer = models.IntegerField()

    class Meta:
        unique_together = ('user', 'question')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'question'], name='unique_user_question')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {self.answer}"

    def clean_answer(self):
        if self.answer < 0 or self.answer >= len(self.question.answers):
            raise ValidationError("El índice de respuesta no es válido.")

    @property
    def is_correct(self):
        return self.question.answers[self.answer]['is_true']
