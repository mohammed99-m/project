from django.db import models
from accounts.models import Profile

class Notification(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_notifications")
    content = models.TextField()
    room_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)