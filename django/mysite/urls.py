from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import login, logout



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('chat.urls')),
]

