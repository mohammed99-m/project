from django.contrib import admin

from illnesses.models import IllnessToAvoidExercises, IllnessToAvoidFood

admin.site.register(IllnessToAvoidExercises)
admin.site.register( IllnessToAvoidFood)
# Register your models here.
