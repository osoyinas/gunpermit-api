from django.db import models
from django.forms import ValidationError


class TopicModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.title

    @property
    def questions_count(self):
        return self.questions.count()


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

        true_count = 0
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

                if key == 'is_true' and received_answer[key]:
                    true_count += 1

        if true_count != 1:
            raise ValidationError("Debe haber exactamente un valor 'true' en 'answers'.")

    @property
    def correct_answer_index(self):
        for index, answer in enumerate(self.answers):
            if answer['is_true']:
                return index
        return None
