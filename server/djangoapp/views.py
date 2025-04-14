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
from .models import CarMake, CarModel, Dealer
from .populate import initiate
from .populate_dealers import populate_dealers
from .restapis import get_request, analyze_review_sentiments, post_review, get_dealers_from_cf
from django.views.decorators.http import require_http_methods


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
            # 尝试解析JSON数据
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                username = data.get('userName')
                password = data.get('password')
                email = data.get('email', '')
            else:
                # 处理表单数据
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email', '')

            if not username or not password:
                return JsonResponse({
                    "error": "Username and password are required"
                }, status=400)
            
            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "error": "Already Registered"
                }, status=400)
            
            # 创建用户
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
            # 登录用户
            login(request, user)
            
            # 设置session
            request.session['username'] = username
            
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON data in registration request")
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({
                "error": str(e)
            }, status=400)
    else:
        return JsonResponse({
            "error": "Only POST method is allowed"
        }, status=405)

# Get dealer reviews by dealer id
def get_dealer_reviews(request, dealer_id):
    """
    Get reviews for a specific dealer with sentiment analysis
    
    Args:
        request: HTTP request
        dealer_id (int): ID of the dealer
    
    Returns:
        JsonResponse: List of reviews with sentiment analysis
    """
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Get all dealers
@require_http_methods(["GET"])
def get_dealers(request):
    try:
        logger.info("Fetching all dealers")
        
        # Check if there are any dealers in the database
        if Dealer.objects.count() == 0:
            logger.info("No dealers found in database, populating with sample data")
            populate_dealers()
            
        # Get all dealers from database
        dealers = Dealer.objects.all()
        dealers_data = []
        
        for dealer in dealers:
            dealers_data.append({
                "id": dealer.id,
                "full_name": dealer.full_name,
                "city": dealer.city,
                "state": dealer.state,
                "address": dealer.address,
                "zip": dealer.zip,
                "web": dealer.web,
                "lat": float(dealer.lat),
                "long": float(dealer.long)
            })
            
        logger.info(f"Retrieved {len(dealers_data)} dealers")
        response = JsonResponse({"status": 200, "dealers": dealers_data})
        response["Content-Type"] = "application/json"
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Credentials"] = "true"
        return response
        
    except Exception as e:
        logger.error(f"Error in get_dealers: {str(e)}")
        return JsonResponse(
            {"status": "error", "message": "Failed to fetch dealers", "error": str(e)},
            status=500
        )

# Get dealer by id
def get_dealer_by_id(request, dealer_id):
    if request.method == "GET":
        try:
            # 使用get_request函数获取特定经销商数据
            dealer = get_request("/api/dealership", dealerId=dealer_id)
            return JsonResponse(dealer)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Get dealers by state
@require_http_methods(["GET"])
def get_dealers_by_state(request, state):
    try:
        logger.info(f"Fetching dealers for state: {state}")
        
        # Get dealers filtered by state
        dealers = Dealer.objects.filter(state__iexact=state)
        dealers_data = []
        
        for dealer in dealers:
            dealers_data.append({
                "id": dealer.id,
                "full_name": dealer.full_name,
                "city": dealer.city,
                "state": dealer.state,
                "address": dealer.address,
                "zip": dealer.zip,
                "web": dealer.web,
                "lat": float(dealer.lat),
                "long": float(dealer.long)
            })
            
        logger.info(f"Found {len(dealers_data)} dealers in state {state}")
        return JsonResponse({"status": 200, "dealers": dealers_data})
        
    except Exception as e:
        logger.error(f"Error in get_dealers_by_state for state {state}: {str(e)}")
        return JsonResponse(
            {"status": "error", "message": f"Failed to fetch dealers for state {state}", "error": str(e)},
            status=500
        )

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

def get_dealerships(request, state="All"):
    """
    Get dealerships by state or all dealerships
    
    Args:
        request: HTTP request
        state (str): State to filter dealerships, "All" for all dealerships
    
    Returns:
        JsonResponse: List of dealerships
    """
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    """
    Get details of a specific dealer
    
    Args:
        request: HTTP request
        dealer_id (int): ID of the dealer
    
    Returns:
        JsonResponse: Dealer details
    """
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

@csrf_exempt
def add_review(request):
    """
    Add a review for a dealer
    
    Args:
        request: HTTP request containing review data
    
    Returns:
        JsonResponse: Status of the review submission
    """
    if request.user.is_anonymous == False:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            if response:
                return JsonResponse({"status": 200, "message": "Review added successfully"})
            else:
                return JsonResponse({"status": 401, "message": "Error in posting review"})
        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "message": "Invalid JSON data"})
        except Exception as e:
            logger.error(f"Error in add_review: {str(e)}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

def about(request):
    """
    View function for about page
    """
    return render(request, 'about.html')

def contact(request):
    """
    View function for contact page
    """
    return render(request, 'contact.html')