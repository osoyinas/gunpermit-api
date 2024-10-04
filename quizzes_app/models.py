from django.db import models
from auth_app.models import CustomUser
from questions_app.models import QuestionModel


class QuizModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    questions = models.ManyToManyField(
        QuestionModel,
        through='QuizQuestionModel',
        related_name='quizzes',
        related_query_name='quiz'
    )

    def __str__(self):
        return self.title


class QuizQuestionModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'question'], name='unique_quiz_question')
        ]


class QuizResultModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quiz.title} - {self.score}'
    
    @property
    def score(self):
        total_questions = self.quiz.questions.count()
        if total_questions == 0:
            return 0
        return (self.correct_answers / total_questions) * 100
    
    @property
    def passed(self):
        return self.score >= 80 # 16/20 80% passing grade
    
    