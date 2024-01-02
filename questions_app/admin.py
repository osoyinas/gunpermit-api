from django.contrib import admin
from .models import TopicModel, SubtopicModel, QuestionModel
# Register your models here.
admin.site.register(TopicModel)
admin.site.register(SubtopicModel)
admin.site.register(QuestionModel)