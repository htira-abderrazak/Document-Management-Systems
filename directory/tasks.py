from celery import Celery

from file.models import File
from .models import Directory

from django.utils import timezone
from django.conf import settings

from datetime import timedelta

import boto3

import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError

import json

from .operations.operation_registry import OPERATION_REGISTRY
from .operations.prompt import prompt

from django.contrib.auth import get_user_model

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import logging

app = Celery()
logger = logging.getLogger(__name__)

#define a 
@app.task
def periodic_delete():
    now = timezone.now()

    # Calculate the time one minute ago with timezone awareness
    expiration_start = now - timedelta(seconds=10)

    folders = Directory.objects.filter(is_deleted = True, updated_at__lte=expiration_start)
    files = File.objects.filter(is_deleted = True, updated_at__lte=expiration_start)
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    paths =[] # store paths to delete them after deleting the 
    for file in files:
        
        paths.append(file.file)
        user = file.user
        totalSize = user.total_size - file.file.size
        user.total_size = totalSize
        file.user.save()
        
    folders.delete()
    files.delete()
    for path in paths :
        try:
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=str(path))
            
        except Exception as e:
            print(f"Error deleting file from S3: {e}")

@app.task
def MCP(message,data_file,user,id):
    # Operations exist or not in the llm response
    operation_exist = False
    User = get_user_model()
    try :
        user = User.objects.get(id=user)
    except User.DoesNotExist :
        print("unkown User")
        return None
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json"

            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat-v3-0324:free",

                "messages": [
                    {
                        "role": "system",
                        "content": prompt(data_file)
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]   
                })
            )
        
        data = response.json() 

    except Timeout:
        logger.error("Request to OpenRouter timed out.")
        send_error_message(operation_exist,user.id)
        return {"error": "The request timed out."}

    except ConnectionError:
        logger.error("Failed to connect to OpenRouter.")
        send_error_message(operation_exist,user.id)
        return {"error": "Connection error."}

    except HTTPError as e:
        logger.error(f"HTTP error occurred: {e} - Response: {e.response.text}")
        send_error_message(operation_exist,user.id)
        return {"error": f"HTTP error: {e.response.status_code}"}

    except RequestException as e:
        logger.error(f"General Request exception: {str(e)}")
        send_error_message(operation_exist,user.id)
        return {"error": "A request exception occurred."}

    except ValueError as e:
        logger.error(f"JSON decoding failed: {str(e)}")
        send_error_message(operation_exist,user.id)
        return {"error": "Failed to parse JSON response."}

    except Exception as e:
        logger.exception("Unexpected error in OpenRouter task.")
        send_error_message(operation_exist,user.id)
        return {"error": "Unexpected error occurred."}
    try: 
        # Parse the string as JSON
        message_content = data["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError) as e:
        print(f"Malformed LLM response structure: {e}, full response: {data}")
        send_error_message(operation_exist,user.id)
        return 
    if not message_content or not isinstance(message_content, str):
        print(f"Empty or invalid message content: {message_content}")
        send_error_message(operation_exist,user.id)
        return 




    # Strip potential markdown formatting
    cleaned_data = message_content.strip()
    if cleaned_data.startswith("```json"):
        cleaned_data = cleaned_data[7:]
    elif cleaned_data.startswith("```"):
        cleaned_data = cleaned_data[3:]
    if cleaned_data.endswith("```"):
        cleaned_data = cleaned_data[:-3]

    try:
        content_json = json.loads(cleaned_data)

        user_message = content_json["message"]
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in message_content: {e}\nRaw content: {cleaned_data}")
        send_error_message(operation_exist,user.id)
        return 
           


    for item in content_json.get("operations", []):
        operation_name = list(item.keys())[0]  
        params = item[operation_name]          

        operation = OPERATION_REGISTRY.get(operation_name)
        if not operation:
            print(f"Unknown operation: {operation_name}")
            continue
        operation_exist=True
        # Inject user if the function expects it
        if "user" in operation.__code__.co_varnames:
            params["user"] = user

        # Inject the parent direvtory if the function expects it
        if "parent_id" in operation.__code__.co_varnames:
            params["parent_id"] = id
        try:
            operation(**params)  # operation is executed here
        except Exception as e:
            print(f"Error executing {operation_name}: {e}")


    send_meesage(user_message,operation_exist,user.id)


def send_meesage(user_message,operations_exist,id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{id}',
        {
            'type': 'send_llm_response',
            'response': f"{user_message}",
            'reload': operations_exist

        }
    )

def send_error_message(operations_exist,id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{id}',
        {
            'type': 'send_error_response',
            'response': f"error",
            'reload': operations_exist
        }
    )