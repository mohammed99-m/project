from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
def get_user_notifications(request, user_id):
    notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)