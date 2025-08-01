"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="توثيق API الخاص بي",
   ),
   public=True,
   authentication_classes=[SessionAuthentication],  # أضف هذا
   permission_classes=[AllowAny],
)

urlpatterns = [
    path('authapp/',include('authapp.urls')),
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('posts/',include('posts.urls')),
    path('exercises/',include('exercises.urls')),
    path('health/',include('health.urls')),
    path('illnesses/',include('illnesses.urls')),
    path('notifications/',include('notifications.urls')),
    path('chatapp/',include('chatapp.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]