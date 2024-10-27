from django.contrib import admin

from tracking_app.models import QuizResultModel, UserQuestionAttemptModel

# Register your models here.
admin.site.register(UserQuestionAttemptModel)
admin.site.register(QuizResultModel)
