
# user/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

# lazily import the serializer and the task once and cache it to avoid Django initialization errors 
from functools import lru_cache
@lru_cache(maxsize=1)
def get_directory_serializer():
    from directory.serializers import DirectoryListSerializer
    return DirectoryListSerializer

@lru_cache(maxsize=1)
def get_process_message_with_llm():
    from directory.tasks import MCP
    return MCP

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        
        # Debug logging
        print(f"User: {user}")
        print(f"User type: {type(user)}")
        print(f"Is authenticated: {user.is_authenticated}")
        print(f"Is anonymous: {user.is_anonymous}")
        
        # Check if user is authenticated
        if user.is_authenticated:
            self.room_group_name = f'chat_{user.id}'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            print(f"Connection accepted for user: {user.id}")
        else:
            print("Connection rejected - user not authenticated")
            await self.close(code=4001)  # Custom close code for authentication failure

    async def disconnect(self, close_code):
        room_group_name = getattr(self, 'room_group_name', None)
        if room_group_name:
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )
            print(f"User left room: {room_group_name}")
    async def receive(self, text_data):
        user = self.scope['user']

        try:
            data = json.loads(text_data)
            message = data['message']
            id = data['id']
            data_content = data['data']

        except json.JSONDecodeError or KeyError :
            await self.close(code=1008)  
            raise StopConsumer("Invalid input")
                    
        DirectoryListSerializer = get_directory_serializer()
        serialized_data=DirectoryListSerializer(data=data_content)
        if not serialized_data.is_valid():
            await self.close(code=1008)
            raise StopConsumer("Invalid serializer data")

        process_message_with_llm = get_process_message_with_llm()
        process_message_with_llm.delay(message,data_content,user.id,id)

    async def send_llm_response(self, event):
        response = event['response']

        await self.send(text_data=json.dumps({
            'response': response
        }))
    async def send_error_response(self, event):
        error_message = event['response']
        await self.send(text_data=json.dumps({
            'error': error_message
        }))
