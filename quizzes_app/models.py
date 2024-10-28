from django.db import models
from auth_app.models import CustomUser
from questions_app.models import QuestionModel
from django.db.models import UniqueConstraint


class QuizCategoryModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'#{self.tag}'


class QuizModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField(
        QuestionModel,
        through='QuizQuestionModel',
        related_name='quizzes',
        related_query_name='quiz'
    )
    category = models.ForeignKey(
        QuizCategoryModel, related_name='quizzes', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            UniqueConstraint(fields=['number', 'category'],
                             name='unique_number_category')
        ]


class QuizQuestionModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['quiz', 'question'], name='unique_quiz_question')
        ]
