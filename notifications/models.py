from django.db import models
from accounts.models import Profile

class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField()
    room_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
