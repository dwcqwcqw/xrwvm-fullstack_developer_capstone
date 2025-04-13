# Uncomment the required imports before adding the code

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # 尝试解析JSON数据（API请求）
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
        except json.JSONDecodeError:
            # 如果不是JSON，则尝试获取表单数据
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            # 设置session中的用户名
            request.session['username'] = username
            if request.content_type == 'application/json':
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                # 在重定向之前设置一个JavaScript，将用户名存入sessionStorage
                response = HttpResponse(
                    f'''
                    <script>
                    sessionStorage.setItem("username", "{username}");
                    window.location.href = "/";
                    </script>
                    '''
                )
                return response
        else:
            if request.content_type == 'application/json':
                return JsonResponse({"userName": username, "status": "Authentication Failed"})
            else:
                messages.error(request, '用户名或密码错误')
                return redirect('/login/')
    else:
        return render(request, 'login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    try:
        # 获取当前用户名
        username = request.user.username
        # 清除session
        logout(request)
        return JsonResponse({"userName": username})
    except:
        return JsonResponse({"error": "Logout failed"}, status=400)

# Create a registration view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            email = data.get('email', '')
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
            # Login the user
            login(request, user)
            
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({"error": "Registration failed"}, status=400)
    else:
        return render(request, 'register.html')