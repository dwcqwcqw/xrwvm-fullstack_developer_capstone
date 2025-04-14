# Uncomment the required imports before adding the code

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel, Dealer
from .populate import initiate
from .populate_dealers import populate_dealers
from .restapis import get_request, analyze_review_sentiments, post_review, get_dealers_from_cf, post_request
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    """Handle user login."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            if not username or not password:
                return JsonResponse(
                    {'userName': None, 'status': 'Missing credentials'},
                    status=400
                )

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse(
                    {'userName': user.username, 'status': 'Authenticated'}
                )
            return JsonResponse(
                {'userName': None, 'status': 'Authentication Failed'},
                status=401
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'userName': None, 'status': 'Invalid JSON'},
                status=400
            )

    return JsonResponse(
        {'userName': None, 'status': 'Method not allowed'},
        status=405
    )

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({'status': 'Logged out'})

# Create a registration view to handle sign up request
@csrf_exempt
def registration(request):
    """Handle user registration."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            if not username or not password:
                return JsonResponse(
                    {'error': 'Missing required fields'},
                    status=400
                )

            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {'error': 'Username already exists'},
                    status=400
                )

            user = User.objects.create_user(
                username=username,
                password=password
            )
            login(request, user)
            return JsonResponse({'status': 'Registration successful'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse(
        {'error': 'Method not allowed'},
        status=405
    )

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
    """Get all dealerships."""
    if request.method == "GET":
        dealers = Dealer.objects.all()
        dealers_data = [
            {
                'id': dealer.id,
                'name': dealer.name,
                'city': dealer.city,
                'state': dealer.state,
                'address': dealer.address,
                'zip': dealer.zip,
                'lat': dealer.lat,
                'long': dealer.long
            }
            for dealer in dealers
        ]
        return JsonResponse({'dealers': dealers_data})

    return JsonResponse(
        {'error': 'Method not allowed'},
        status=405
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
    """Get all cars."""
    car_makes = CarMake.objects.all()
    car_models = CarModel.objects.all()

    makes_data = [
        {
            'id': make.id,
            'name': make.name,
            'description': make.description
        }
        for make in car_makes
    ]

    models_data = [
        {
            'id': model.id,
            'make': model.car_make.name,
            'name': model.name,
            'type': model.type,
            'year': model.year
        }
        for model in car_models
    ]

    return JsonResponse({
        'makes': makes_data,
        'models': models_data
    })

def get_dealerships(request, state="All"):
    """Get dealerships by state or all dealerships."""
    endpoint = f"/fetchDealers/{state}" if state != "All" else "/fetchDealers"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_details(request, dealer_id):
    """Get details for a specific dealer."""
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        dealer_data = {
            'id': dealer.id,
            'name': dealer.name,
            'city': dealer.city,
            'state': dealer.state,
            'address': dealer.address,
            'zip': dealer.zip,
            'lat': dealer.lat,
            'long': dealer.long
        }
        return JsonResponse(dealer_data)
    except Dealer.DoesNotExist:
        return JsonResponse({'error': 'Dealer not found'}, status=404)

@require_http_methods(["POST"])
def add_review(request):
    """Add a new review."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = [
                'name', 'dealership', 'review', 'purchase',
                'purchase_date', 'car_make', 'car_model', 'car_year'
            ]

            if not all(field in data for field in required_fields):
                return JsonResponse(
                    {'error': 'Missing required fields'},
                    status=400
                )

            # Process review data here
            return JsonResponse({'status': 'Review added successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse(
        {'error': 'Method not allowed'},
        status=405
    )

def about(request):
    """About page view."""
    return render(request, 'djangoapp/about.html')

def contact(request):
    """Contact page view."""
    return render(request, 'djangoapp/contact.html')

def get_csrf_token(request):
    """Get CSRF token."""
    return JsonResponse({'csrfToken': 'token'})

def current_user(request):
    """Get current user info."""
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username})
    return JsonResponse({'username': None})