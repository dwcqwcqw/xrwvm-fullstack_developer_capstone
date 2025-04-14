# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

load_dotenv()

# Use the environment variable set in docker-compose, default to the service name
backend_url = os.getenv(
    'DATABASE_API_URL', default="http://localhost:3030")

# Sentiment analyzer service URL
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://sentiment_analyzer:8080")

def get_request(url, **kwargs):
    """Send GET request to the specified URL."""
    try:
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            **kwargs
        )
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None


def post_request(url, payload, **kwargs):
    """Send POST request to the specified URL."""
    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=payload,
            **kwargs
        )
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_dealers_from_cf(url, **kwargs):
    """Get dealers data from the specified URL."""
    results = get_request(url, **kwargs)
    if results:
        dealers = []
        for dealer in results:
            dealer_obj = CarDealer(
                id=dealer.get("id"),
                city=dealer.get("city"),
                state=dealer.get("state"),
                st=dealer.get("st"),
                address=dealer.get("address"),
                zip=dealer.get("zip"),
                lat=dealer.get("lat"),
                long=dealer.get("long"),
                short_name=dealer.get("short_name"),
                full_name=dealer.get("full_name")
            )
            dealers.append(dealer_obj)
        return dealers
    return []


def get_dealer_by_id_from_cf(url, dealerId):
    """Get dealer details by ID from the specified URL."""
    results = get_request(f"{url}/{dealerId}")
    if results:
        dealer = CarDealer(
            id=results.get("id"),
            city=results.get("city"),
            state=results.get("state"),
            st=results.get("st"),
            address=results.get("address"),
            zip=results.get("zip"),
            lat=results.get("lat"),
            long=results.get("long"),
            short_name=results.get("short_name"),
            full_name=results.get("full_name")
        )
        return dealer
    return None


def get_dealer_reviews_from_cf(url, dealerId):
    """Get dealer reviews from the specified URL."""
    results = get_request(f"{url}?dealerId={dealerId}")
    if results:
        reviews = []
        for review in results:
            reviews.append({
                "id": review.get("id"),
                "name": review.get("name"),
                "dealership": review.get("dealership"),
                "review": review.get("review"),
                "purchase": review.get("purchase"),
                "purchase_date": review.get("purchase_date"),
                "car_make": review.get("car_make"),
                "car_model": review.get("car_model"),
                "car_year": review.get("car_year")
            })
        return reviews
    return []

def analyze_review_sentiments(text):
    """
    Analyze sentiment of a given text
    
    Args:
        text (str): Text to analyze
    
    Returns:
        dict: Sentiment analysis result
    """
    try:
        response = requests.post(sentiment_analyzer_url, json={'text': text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {str(e)}")
        return {'sentiment': 'neutral'}

def post_review(data_dict):
    """
    Post a review to the backend database service
    
    Args:
        data_dict (dict): Review data to post
    
    Returns:
        dict: Response from the backend database service or None on failure
    """
    request_url = f"{backend_url}/insert_review"
    print(f"Posting review to database service: {request_url}")
    try:
        # 添加headers以确保正确的Content-Type
        headers = {'Content-Type': 'application/json'}
        print(f"Sending POST request with data: {json.dumps(data_dict)}")
        response = requests.post(request_url, json=data_dict, headers=headers)
        print(f"Database service response status: {response.status_code}")
        
        try:
            print(f"Database service response content: {response.text}") 
        except Exception as print_err:
            print(f"Could not print database service response content: {print_err}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {str(e)}")
        return None

def get_dealers_from_cf():
    """
    Get all dealers from the backend service
    
    Returns:
        list: List of dealers or None if request fails
    """
    request_url = f"{backend_url}/get_dealers"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {str(e)}")
        return None

# def post_review(data_dict):
# Add code for posting review
