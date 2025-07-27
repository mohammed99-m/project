from django.db import models
from accounts.models import Profile

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_messages")
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
