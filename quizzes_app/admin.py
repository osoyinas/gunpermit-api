from django.contrib import admin
from .models import QuizModel, QuestionModel, QuizQuestionModel

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestionModel
    extra = 1

class QuizModelAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]

admin.site.register(QuizModel, QuizModelAdmin)