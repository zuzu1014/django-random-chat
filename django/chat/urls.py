# chat/urls.py
from django.urls import path

from . import views



urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('chat/', views.chat, name='index'),
    path('chat_test/', views.chat_test, name='index'),
    # path('chat/<str:room_name>/', views.room, name='room'),
]