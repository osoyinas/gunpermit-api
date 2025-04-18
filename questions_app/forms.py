from django import forms
from .models import QuestionModel

TEXTAREA_STYLE = {
    'rows': 3,
    'style': 'width: 100%; overflow: hidden; resize: vertical;'
}


class QuestionForm(forms.ModelForm):
    answer_1 = forms.CharField(
        label="Respuesta 1", required=False,
        widget=forms.Textarea(attrs=TEXTAREA_STYLE)
    )
    is_true_1 = forms.BooleanField(label="¿Correcta?", required=False)

    answer_2 = forms.CharField(
        label="Respuesta 2", required=False,
        widget=forms.Textarea(attrs=TEXTAREA_STYLE)
    )
    is_true_2 = forms.BooleanField(label="¿Correcta?", required=False)

    answer_3 = forms.CharField(
        label="Respuesta 3", required=False,
        widget=forms.Textarea(attrs=TEXTAREA_STYLE)
    )
    is_true_3 = forms.BooleanField(label="¿Correcta?", required=False)

    class Meta:
        model = QuestionModel
        fields = ['topic', 'question']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        answers = self.instance.answers if self.instance.answers else []
        for i, ans in enumerate(answers[:3]):
            self.fields[f'answer_{i+1}'].initial = ans.get('answer', '')
            self.fields[f'is_true_{i+1}'].initial = ans.get('is_true', False)

    def clean(self):
        cleaned_data = super().clean()
        answers = []
        for i in range(1, 4):
            answer = cleaned_data.get(f'answer_{i}')
            is_true = cleaned_data.get(f'is_true_{i}', False)
            if answer:
                answers.append({'answer': answer, 'is_true': is_true})
        cleaned_data['answers'] = answers
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.answers = self.cleaned_data.get('answers', [])
        if commit:
            instance.save()
        return instance
