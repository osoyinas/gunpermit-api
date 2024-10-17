from django.db import models


class PlaceModel (models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name + ' - '
    def get_assessments(self):
        return self.assessmentmodel_set.all()

class AssessmentModel (models.Model):
    title = models.CharField(max_length=100)
    place = models.ForeignKey(PlaceModel, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.place.name + ' - ' + str(self.date)
