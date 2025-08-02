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

@api_view(['POST'])
def save_notification2(request):
    sender_id = request.data.get('sender')
    receiver_id = request.data.get('receiver')
    try:
        sender = Profile.objects.get(user__id=sender_id)
        receiver = Profile.objects.get(user__id=receiver_id)
    except Profile.DoesNotExist as e:
        return Response({"error": str(e)}, status=404)

    print(f"Resolved sender: {sender.id}, receiver: {receiver.id}")

    content = request.data.get('content')
    room_name = request.data.get('room_name')

    notification = Notification.objects.create(
        sender=sender,
        receiver=receiver,
        content=content,
        room_name=room_name
    )

    print(f"Notification created with sender id: {notification.sender.id}, receiver id: {notification.receiver.id}")

    return Response({"message": "Notification saved successfully"}, status=201)