from django.contrib import admin

from assessments_app.models import AssessmentModel, PlaceModel

# Register your models here.
admin.site.register(PlaceModel)
admin.site.register(AssessmentModel)