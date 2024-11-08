from django.contrib import admin

from questions_app.forms import QuestionForm

from .models import QuestionModel, TopicModel
from django_json_widget.widgets import JSONEditorWidget
from django.db.models import JSONField

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = ('id', 'topic', 'question')
    list_filter = ('topic',)
    search_fields = ('question',)
    ordering = ('id',)
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

admin.site.register(QuestionModel, QuestionAdmin)
admin.site.register(TopicModel)