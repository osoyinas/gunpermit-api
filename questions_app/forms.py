from django import forms
from .models import QuestionModel
from django.core.exceptions import ValidationError


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ['question', 'topic', 'answers']

    def clean_answers(self):
        # Obtiene las respuestas del formulario
        answers = self.cleaned_data.get('answers')
        self.instance.answers = answers
        # Llama al método 'clean_answers' del modelo para realizar las validaciones
        self.instance.clean_answers()

        return answers
