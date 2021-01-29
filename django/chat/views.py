# chat/views.py
from django.shortcuts import render

from .models import Room
from user.decorators import *
from django.utils.decorators import method_decorator

def index(request):
    
    return render(request, 'chat/index.html', {})


@login_required
def chat(request):
    
    return render(request, 'chat/chat.html', {})
    
    
@login_required
def chat_test(request):
    
    return render(request, 'chat/chat_test.html', {})
    
def lobby(request):
    
    return render(request, 'chat/lobby.html', {})