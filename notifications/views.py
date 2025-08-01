from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Profile
from .serializers import NotificationSerializer
from .models import Notification
from django.contrib.auth import get_user_model

#حفظ الاشعار لاستعماله في السيرفر الثاني
@api_view(['POST'])
def save_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Notification saved successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#عرض الاشعارات بالنسبة لمستخدم محدد
@api_view(['GET'])
def get_user_notifications(request, receiver_id):
    notifications = Notification.objects.filter(receiver_id=receiver_id).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotificationSerializer
from .models import Notification

@api_view(['POST'])
def save_notification2(request):
    sender_id = request.data.get('sender')
    receiver_id = request.data.get('receiver')

    try:
        sender = Profile.objects.get(User__id=sender_id)
        receiver = Profile.objects.get(User__id=receiver_id)
    except User.DoesNotExist:
        return Response({"error": "Sender or receiver not found"}, status=status.HTTP_404_NOT_FOUND)

    # باقي البيانات (مثلاً: content و room_name)
    content = request.data.get('content')
    room_name = request.data.get('room_name')

    notification = Notification.objects.create(
        sender=sender,
        receiver=receiver,
        content=content,
        room_name=room_name
    )

    return Response({"message": "Notification saved successfully"}, status=status.HTTP_201_CREATED)
