from django.contrib import admin
from .models import TopicModel, QuestionModel
# Register your models here.
admin.site.register(TopicModel)
admin.site.register(QuestionModel)