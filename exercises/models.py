from django.db import models

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)  # INT, PRIMARY KEY, AUTO_INCREMENT
    name = models.CharField(max_length=255)  # VARCHAR
    muscle_group = models.CharField(max_length=255)  # VARCHAR
    #video_url = models.URLField(blank=True, null=True)  # URL
    description = models.TextField(blank=True, null=True)  # TEXT

    def __str__(self):
        return self.name