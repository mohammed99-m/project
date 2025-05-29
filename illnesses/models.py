from django.db import models

# Create your models here.
class IllnessToAvoidFood(models.Model):
    illness = models.CharField(max_length=256)
    foods_to_avoid =models.JSONField(default=list)
    sources = models.JSONField(default=list)

class IllnessToAvoidExercises(models.Model):
    illness = models.CharField(max_length=256)
    exercise_to_avoid =models.JSONField(default=list)
    safer_alternatives = models.JSONField(default=list)
    sources = models.JSONField(default=list)
