from celery import Celery

from file.models import File
from .models import Directory

from django.utils import timezone
from django.conf import settings

from datetime import timedelta

import boto3

import requests
import json

from .operations.operation_registry import OPERATION_REGISTRY

from django.contrib.auth import get_user_model

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

app = Celery()

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
    channel_layer = get_channel_layer()

    User = get_user_model()
    try :
        user = User.objects.get(id=user)
    except User.DoesNotExist :
        print("unkown User")
        return None
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json"

        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-lite-001",

            "messages": [
                {
                    "role": "system",
                    "content": f"""You are a file management assistant inside a web application like Google Drive. The user is currently located in a specific folder and this is it content of it : {str(data_file)}. You must not access or manege the subfolders.

            IMPORTANT Rules before respons:
            - Only respond with a valid JSON object — no extra text or explanation.
            - Only refer to items in the current directory using their given IDs.
            - Do not respond to any user request that asks something unrelated to file and folder management.
            - Don't create a folder if a folder with the same name already exists.
            - Do not create files.
            - Do not create a folder and then move an other folder or a file to it always use the move_folder_and_create_destination or move_file_and_create_destination instead

            Your job is to:
            1. Understand what the user wants.
            2. Identify the relevant items from the current directory by their name or type (the content of the directory is given above).
            3. Create a structured response in pure JSON format, with:
                - A "message" field that explains in plain language what action you took.
                - An "operations" field that contains one or more operations to perform, using only the methods listed below, with the correct arguments (you always put an id that provided you from the content of the current folder i gave you do not give an id you create you provide only the names of the files or folders you manage ):

            - create_folder(name, optional parent_id, user)
            - update_folder(folder_id, new_name)
            - update_file(file_id, new_name)
            - move_folder(folder_id, folder_destination_id): use this method when the destination folder already exists (not when you create the folder your self , use this only when the folder is already given to you )
            - move_file(file_id, folder_destination_id): use this method when the destination folder already exists (not when you create the folder your self , use this only when the folder is already given to you )
            - move_folder_and_create_destination(folder_id, new_folder_name, parent_id, user): use this method when the destination folder is created within this request (do not perform this method if a folder with the same name already exists in the current directory)
            - move_file_and_create_destination(file_id, new_folder_name, parent_id, user): same condition as above
            - delete_folder(folder_id)
            - delete_file(file_id)
            - favorite_folder(folder_id, is_favorite)
            - favorite_file(file_id, is_favorite)


            Return the response as **pure JSON only**. Do not include any text before or after it. **Do not wrap the response in ```json or ``` at all**.

            Your response must always be: {{
            "message": "Marking all files as favorite",
            "operations": [
                {{
                "favorite_file": {{
                    "file_id": "70ae6350-73cf-4f86-83fd-d87ecacf3c28",
                    "is_favorite": true
                }}
                }},
                {{
                "favorite_file": {{
                    "file_id": "b7025bc2-362f-47af-a83c-8f853baa64d9",
                    "is_favorite": true
                }}
                }},
                {{
                "favorite_file": {{
                    "file_id": "ee6acd9f-37ae-485b-a93e-f5f033a7b925",
                    "is_favorite": true
                }}
                }}
            ]
            }}"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ]   
            })
        )
    
    data = response.json() 
    try: 
        # Parse the string as JSON
        message_content = data["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError) as e:
        print(f"Malformed LLM response structure: {e}, full response: {data}")
        async_to_sync(channel_layer.group_send)(
            f'chat_{user.id}',
            {
                'type': 'send_error_response',
                'response': f"error"
            }
        )
        return 
    if not message_content or not isinstance(message_content, str):
        print(f"Empty or invalid message content: {message_content}")
        async_to_sync(channel_layer.group_send)(
            f'chat_{user.id}',
            {
                'type': 'send_error_response',
                'response': f"error"
            }
        )
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
        async_to_sync(channel_layer.group_send)(
            f'chat_{user.id}',
            {
                'type': 'send_error_response',
                'response': f"error"
            }
        )
        return 
           


    for item in content_json.get("operations", []):
        operation_name = list(item.keys())[0]  
        params = item[operation_name]          

        operation = OPERATION_REGISTRY.get(operation_name)
        if not operation:
            print(f"Unknown operation: {operation_name}")
            continue

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


    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{user.id}',
        {
            'type': 'send_llm_response',
            'response': f"{user_message}"
        }
    )

