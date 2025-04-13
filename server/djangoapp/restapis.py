# Uncomment the imports below before you add the function code
# import requests
import os
from dotenv import load_dotenv
import requests
import json
from django.conf import settings

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    发送GET请求到指定的端点
    
    Args:
        endpoint (str): 请求的端点URL
        **kwargs: URL参数，如dealerId等
    
    Returns:
        dict: 响应数据
    """
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params = params + key + "=" + str(value) + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        # 调用requests库的get方法，传入URL和参数
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        # 如果发生任何错误
        print("Network exception occurred: ", str(e))
        return {"error": str(e)}

def analyze_review_sentiments(text):
    """
    分析评论的情感
    
    Args:
        text (str): 要分析的评论文本
    
    Returns:
        dict: 情感分析结果
    """
    request_url = sentiment_analyzer_url + text
    try:
        # 调用requests库的get方法，传入URL
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"error": str(err)}

# def post_review(data_dict):
# Add code for posting review
