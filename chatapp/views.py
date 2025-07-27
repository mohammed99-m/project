from chatapp.serializers import MessageSerializer
from .models import Profile
from .models import Message
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
#حفظ الرسالة 
@api_view(['POST'])
def save_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Message saved successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#عرض الرسالة للغرفة الخاصة بالمرسل والمستلم
@api_view(['GET'])
def get_messages(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)