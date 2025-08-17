from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
<<<<<<< HEAD
        fields = ['sender', 'receiver','room_name', 'content', 'timestamp','room_id']
=======
        fields = ['sender', 'receiver','room_name', 'content', 'timestamp','room_id']
>>>>>>> origin/main
