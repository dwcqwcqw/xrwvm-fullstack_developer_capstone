# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# Use the environment variable set in docker-compose, default to the service name
backend_url = os.getenv(
    'DATABASE_API_URL', default="http://localhost:3030")

# Sentiment analyzer service URL
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://sentiment_analyzer:8080")

def get_request(url, **kwargs):
    """
    Send GET request to the specified endpoint
    
    Args:
        url (str): The endpoint URL
        **kwargs: Additional parameters for the request
    
    Returns:
        dict: Response data
    """
    try:
        # 确保URL是完整的
        if not url.startswith('http'):
            url = f"{backend_url}{url}"
        print(f"Sending GET request to: {url}")
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {str(e)}")
        return None

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
