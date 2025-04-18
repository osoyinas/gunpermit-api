from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import QuizModel, QuizQuestionModel, QuizCategoryModel


class QuizResource(resources.ModelResource):
    class Meta:
        model = QuizModel


class QuizCategoryResource(resources.ModelResource):
    class Meta:
        model = QuizCategoryModel


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestionModel
    extra = 0
    ordering = ['order']
    readonly_fields = ['question_text', 'question_topic', 'formatted_answers']
    fields = ['order', 'question', 'question_text', 'question_topic', 'formatted_answers']

    def question_text(self, obj):
        return obj.question.question if obj.question else "-"
    question_text.short_description = "Texto de la pregunta"

    def question_topic(self, obj):
        return obj.question.topic.title if obj.question and obj.question.topic else "-"
    question_topic.short_description = "Tema"

    def formatted_answers(self, obj):
        if obj.question and obj.question.answers:
            try:
                return "\n".join(
                    f"- {'✅' if a.get('is_true') else '❌'} {a.get('answer')}" 
                    for a in obj.question.answers
                )
            except Exception as e:
                return f"Error leyendo respuestas: {e}"
        return "-"
    formatted_answers.short_description = "Respuestas"


@admin.register(QuizModel)
class QuizAdmin(ImportExportModelAdmin):
    resource_class = QuizResource
    list_display = ['title', 'number', 'category', 'created_at']
    list_filter = ('category',)
    search_fields = ('title', 'number')
    inlines = [QuizQuestionInline]
    ordering = ["number", "title"]


@admin.register(QuizCategoryModel)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = QuizCategoryResource
    list_display = ["title", "description", "tag"]
