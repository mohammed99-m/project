from django.contrib import admin
from .models import Exercise, ExerciseSchedule ,Program
admin.site.register(Exercise)
admin.site.register(Program)
admin.site.register(ExerciseSchedule)