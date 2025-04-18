from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from questions_app.forms import QuestionForm
from .models import QuestionModel, TopicModel


class QuestionResource(resources.ModelResource):
    class Meta:
        model = QuestionModel


class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    form = QuestionForm
    list_display = ('id', 'topic', 'question', 'formatted_answers')
    list_filter = ('topic',)
    search_fields = ('question',)
    ordering = ('id',)

    @admin.display(description="Respuestas")
    def formatted_answers(self, obj):
        if not obj.answers:
            return "-"
        html = "<ul style='margin: 0; padding-left: 1.2em;'>"
        for ans in obj.answers:
            check = "✅" if ans.get("is_true") else "❌"
            answer_text = ans.get("answer", "")
            html += f"<li>{check} {answer_text}</li>"
        html += "</ul>"
        return mark_safe(html)


admin.site.register(QuestionModel, QuestionAdmin)
admin.site.register(TopicModel)
