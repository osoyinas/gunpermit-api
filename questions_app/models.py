from django.db import models
from django.forms import ValidationError
from auth_app.models import CustomUser


class TopicModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " (ID: " + str(self.id) + ")"


ANSWERS_STRUCTURE = [{'answer': str, 'is_true': bool}] * 3
DEFAULT_ANSWERS = [{'answer': "respuesta", 'is_true': False}] * 3


class QuestionModel(models.Model):
    question = models.TextField(max_length=300)
    answers = models.JSONField(default=list)
    topic = models.ForeignKey(
        TopicModel, on_delete=models.CASCADE, related_name="questions")

    def clean_answers(self):
        if not isinstance(self.answers, list):
            raise ValidationError("El campo 'answers' debe ser una lista.")
        if len(self.answers) != len(ANSWERS_STRUCTURE):
            raise ValidationError(
                f"El campo 'answers' debe tener exactamente {len(ANSWERS_STRUCTURE)} elementos.")

        for expected_answer, received_answer in zip(ANSWERS_STRUCTURE, self.answers):
            if not isinstance(received_answer, dict):
                raise ValidationError(
                    "Cada elemento en 'answers' debe ser un diccionario.")

            for key, expected_type in expected_answer.items():
                if key not in received_answer:
                    raise ValidationError(
                        f"Falta la clave '{key}' en uno de los elementos de 'answers'.")

                if not isinstance(received_answer[key], expected_type):
                    raise ValidationError(
                        f"El valor de '{key}' en 'answers' debe ser de tipo {expected_type}.")


class UserQuestionAttemptModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="question_attempts")
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name="user_attempts")
    answer = models.IntegerField()
    class Meta:
        unique_together = ('user', 'question')
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_user_question')
        ]
        

    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {self.answer}"
    
    def clean_answer(self):
        if self.answer < 0 or self.answer >= len(self.question.answers):
            raise ValidationError("El índice de respuesta no es válido.")

    @property
    def is_correct(self):
        return self.question.answers[self.answer]['is_true']
        