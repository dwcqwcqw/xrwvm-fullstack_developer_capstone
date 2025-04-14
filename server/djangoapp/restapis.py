# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# Get backend API URL from environment variables
backend_url = os.environ.get('BACKEND_URL', 'http://localhost:3000')

# Sentiment analyzer service URL
sentiment_analyzer_url = os.environ.get('SENTIMENT_ANALYZER_URL', 'https://sentianalyzer.1u77iwazlgxa.us-south.codeengine.appdomain.cloud/analyze/')

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
    Post a review to the backend
    
    Args:
        data_dict (dict): Review data to post
    
    Returns:
        dict: Response from the backend
    """
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
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
