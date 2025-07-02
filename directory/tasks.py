from celery import Celery

from file.models import File
from .models import Directory

from django.utils import timezone
from django.conf import settings

from datetime import timedelta

import boto3

import requests
import json

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
def MCP(message,data_file,user):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json"

        },
        data=json.dumps({
            "model": "mistralai/mistral-small-3.2-24b-instruct:free",
             "messages": [
                {
                    "role": "system",
                    "content": "You are a file management assistant inside a web application like Google Drive. The user is currently located in a specific folder and this is the content of the folder: "+str(data_file)+". You are only allowed to create, update, move, delete, or favorite files and folders that are directly inside this current directory. You must not access subfolders or files inside them. You will always receive: - A list of the contents of the current directory (files and folders, with their names and unique IDs). - An instruction from the user (such as 'move the images to folder2' or 'delete file3'). Your job is to: 1. Understand what the user wants. 2. Identify the relevant items from the current directory by their name or type. 3. Create a structured response in pure JSON format, with: - A 'message' field that explains in plain language what action you took. - A 'operations' field that contains one or more operations to perform, using only the methods listed below, with the correct arguments (you must use the correct id from the current directory content): here is the Allowed Operations and the explanation when to use : -create_folder(name, optional parent_id, user) – update_folder(folder_id, new_name) – update_file(file_id, new_name) – move_folder_to_existing_folder(folder_id, destination_id) : use this method when the destination folder already exists – move_file_to_existing_folder(file_id, destination_id) : use this method when the destination folder already exists – move_folder_after_creating_destination_folder(folder_id, new_folder_name, parent_id, user) : use this method when the destination folder is created within this request (do not perform this methode if a folder with the same name is already exist in the current directory) – move_file_after_creating_destination_folder(file_id, new_folder_name, parent_id, user) : use this method when the destination folder is created within this request (do not perform this methode if a folder with the same name is already exist in the current directory) – delete_folder(folder_id) – delete_file(file_id) – favorite_folder(folder_id, is_favorite) – favorite_file(file_id, is_favorite). IMPORTANT Rules: - Only respond with a valid JSON object — no extra text or explanation. - Only refer to items in the current directory using their given IDs. - Do not invent any data or access folders/files that were not provided - Do not respond to any user request that asks something unrelated to file and folder management - don t create a folder that it s name already exist - Do not move a file or folder unless the destination folder ID is already present in the current folder’s contents - the methodes 'create_folder' and 'move_file_after_creating_destination_folder' or 'move_folder_after_creating_destination_folder' ,must not be in the response if they have the same name - do not create files.Example of your response format:{ 'message': 'creating a folder named files and deplacing all the files to it', 'methodes': [ { 'move_file_after_creating_destination_folder': { 'file_id': 'abc123', 'parent_id': 'xyz456',folder_name:'xyz' } } ] }"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]   
            })
        )
    data = response.json()
    print(data["choices"][0]["message"]["content"])




