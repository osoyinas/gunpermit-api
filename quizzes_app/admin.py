from django.contrib import admin
from .models import QuizCategoryModel, QuizModel, QuizQuestionModel, QuizResultModel


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestionModel
    extra = 1


class QuizModelAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]
    list_filter = ('category',)  # Agrega el filtro por categoría
    list_display = ('title', 'category', 'number',
                    'num_questions')  # Agrega columnas

    def num_questions(self, obj):
        return obj.quizquestionmodel_set.count()
    num_questions.short_description = 'Number of Questions'


admin.site.register(QuizModel, QuizModelAdmin)
admin.site.register(QuizResultModel)
admin.site.register(QuizCategoryModel)
