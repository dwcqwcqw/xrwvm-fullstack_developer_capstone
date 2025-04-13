# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import requests
import json
from django.conf import settings

load_dotenv()

# Backend API base URL
backend_url = os.getenv(
    "backend_url",
    default="http://localhost:3000/")

# Sentiment analyzer service URL
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    default="https://sentianalyzer.1u77iwazlgxa.us-south.codeengine.appdomain.cloud/analyze/")

def get_request(endpoint, **kwargs):
    """
    Send GET request to the specified endpoint
    
    Args:
        endpoint (str): The endpoint URL to request
        **kwargs: URL parameters such as dealerId
    
    Returns:
        dict: Response data
    """
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params = params + key + "=" + str(value) + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        # If any error occurs
        print("Network exception occurred: ", str(e))
        return {"error": str(e)}

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of a review
    
    Args:
        text (str): The review text to analyze
    
    Returns:
        dict: Sentiment analysis result
    """
    request_url = sentiment_analyzer_url + text
    try:
        # Call get method of requests library with URL
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"error": str(err)}

# def post_review(data_dict):
# Add code for posting review
