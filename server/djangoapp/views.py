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
from django.middleware.csrf import get_token


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    """Handle user login requests."""
    if request.method != "POST":
        return render(request, 'login.html')

    try:
        # Try to parse JSON data (API request)
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
    except json.JSONDecodeError:
        # If not JSON, try to get form data
        username = request.POST.get('username')
        password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        request.session['username'] = username
        
        if request.content_type == 'application/json':
            return JsonResponse({
                "userName": username,
                "status": "Authenticated"
            })
        
        response = HttpResponse(
            f'''
            <script>
            sessionStorage.setItem("username", "{username}");
            window.location.href = "/";
            </script>
            '''
        )
        return response
    
    if request.content_type == 'application/json':
        return JsonResponse({
            "userName": username,
            "status": "Authentication Failed"
        })
    
    messages.error(request, 'Invalid username or password')
    return redirect('/login/')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """Handle user logout requests."""
    try:
        username = request.user.username
        logout(request)
        return JsonResponse({"userName": username})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return JsonResponse({"error": "Logout failed"}, status=400)

# Create a registration view to handle sign up request
@csrf_exempt
def registration(request):
    """Handle user registration requests."""
    if request.method != "POST":
        return JsonResponse({
            "error": "Only POST method is allowed"
        }, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        email = data.get('email', '')

        if not username or not password:
            return JsonResponse({
                "error": "Username and password are required"
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "error": "Already Registered"
            }, status=400)

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        login(request, user)
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
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    if reviews is None:
        logger.error(f"Failed to fetch reviews for dealer {dealer_id} from backend service.")
        return JsonResponse({"status": 500, "message": "Failed to fetch reviews from backend service"})

    if not isinstance(reviews, list):
        logger.error(f"Unexpected response format for reviews from backend service: {reviews}")
        return JsonResponse({"status": 500, "message": "Unexpected response format for reviews"})

    # Initialize sentiment analysis results list
    reviews_with_sentiment = []

    # Perform sentiment analysis for each review
    for review_detail in reviews:
        try:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', 'neutral')  # Default to neutral if analysis fails
        except Exception as e:
            logger.error(f"Error analyzing sentiment for review {review_detail.get('id')}: {str(e)}")
            review_detail['sentiment'] = 'neutral'  # Default to neutral on error
        reviews_with_sentiment.append(review_detail)
    
    return JsonResponse({"status": 200, "reviews": reviews_with_sentiment})

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
    """Get all car models with their makes."""
    if not CarMake.objects.exists():
        initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        }
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})

def get_dealerships(request, state="All"):
    """Get dealerships by state or all dealerships."""
    endpoint = f"/fetchDealers/{state}" if state != "All" else "/fetchDealers"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_details(request, dealer_id):
    """Get details of a specific dealer."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        dealer_data = {
            "id": dealer.id,
            "full_name": dealer.full_name,
            "city": dealer.city,
            "state": dealer.state,
            "address": dealer.address,
            "zip": dealer.zip,
            "web": dealer.web,
            "lat": float(dealer.lat),
            "long": float(dealer.long)
        }
        return JsonResponse({"status": 200, "dealer": [dealer_data]})
    except Dealer.DoesNotExist:
        return JsonResponse({
            "status": 404,
            "message": "Dealer not found"
        })
    except Exception as e:
        logger.error(f"Error in get_dealer_details: {str(e)}")
        return JsonResponse({
            "status": 500,
            "message": f"Server error: {str(e)}"
        })

@require_http_methods(["POST"])
def add_review(request):
    """Add a review for a dealer."""
    if not request.user.is_authenticated:
        logger.warning("Unauthenticated user attempted to post review")
        return JsonResponse({
            "status": 401,
            "message": "Please login to post a review",
            "error_type": "authentication"
        })

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data in request: {str(e)}")
        return JsonResponse({
            "status": 400,
            "message": "Invalid JSON data",
            "error_type": "invalid_format"
        })

    required_fields = [
        'name', 'dealership', 'review',
        'car_make', 'car_model', 'car_year',
        'purchase_date'
    ]
    missing_fields = [
        field for field in required_fields
        if field not in data or not data[field]
    ]

    if missing_fields:
        logger.warning(
            f"Missing required fields in review submission: {missing_fields}"
        )
        return JsonResponse({
            "status": 400,
            "message": f"Missing required fields: {', '.join(missing_fields)}",
            "error_type": "missing_fields",
            "missing_fields": missing_fields
        })

    try:
        dealer = Dealer.objects.get(id=data['dealership'])
        # Process review data here
        return JsonResponse({
            "status": 201,
            "message": "Review submitted successfully"
        })
    except Dealer.DoesNotExist:
        logger.error(f"Dealer with ID {data['dealership']} not found")
        return JsonResponse({
            "status": 404,
            "message": f"Dealer with ID {data['dealership']} not found",
            "error_type": "dealer_not_found"
        })

def about(request):
    """View function for about page."""
    return render(request, 'about.html')

def contact(request):
    """View function for contact page."""
    return render(request, 'contact.html')

def get_csrf_token(request):
    """Get CSRF token."""
    return JsonResponse({'csrfToken': get_token(request)})

def current_user(request):
    """Get current user's login status."""
    return JsonResponse({
        'isLoggedIn': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })