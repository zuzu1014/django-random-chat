from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from django.contrib.auth.decorators import login_required

from .models import *
from user.decorators import *
from django.utils.decorators import method_decorator
from django.contrib import auth


def index(request):
    return render(request, 'common/index.html', {})

@method_decorator(logout_required, name='dispatch')
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html', {})
    
    def post(self, request):
        try:
            user_id = request.POST.get("user_id",None)
            password = request.POST.get("password",None)
            
            user = auth.authenticate(request, user_id=user_id, password=password)
            
            if user is not None:
                auth.login(request, user)
                return JsonResponse({'msg': "success"}, status=200)
            else:
                return JsonResponse({'msg': "mismatch"}, status=200)

        
        except:
            return JsonResponse({'msg': "error"}, status=200)

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")
    
@method_decorator(logout_required, name='dispatch')
class RegisterView(View):
    def get(self,request):
        return render(request, 'user/register.html', {})
    
    def post(self,request):
        try:
            user_id = request.POST.get('user_id',None)
            password = request.POST.get('password',None)
            email = request.POST.get('email',None)
            
            user = User.objects.create_user(user_id=user_id,password=password,email=email)
            
            auth.login(request, user)
            
            return JsonResponse({'msg': "success"}, status=200)

        except:
            return JsonResponse({'msg': "error"}, status=200)


def check_unique_id(request):
    try:
        user_id = request.POST.get('user_id',None)
        
        print(user_id)

        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({'msg': "duplicate"}, status=200)
        
        else:
            return JsonResponse({'msg': "success"}, status=200)
        
    except KeyError:
        return JsonResponse({'msg': "INVALID_KEYS"}, status=400)
    
@method_decorator(login_required, name='dispatch')
class MypageView(View):
    def get(self,request):
        return render(request, 'user/mypage.html')
        