
# user/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


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

        if not user.is_authenticated:
            # Optionally close connection or ignore the message
            await self.close()
            return
        from directory.tasks import process_message_with_llm
        data = json.loads(text_data)
        message = data['message']
        

        # Call Celery task
        process_message_with_llm.delay(user.id, message)

    async def send_llm_response(self, event):
        response = event['response']

        await self.send(text_data=json.dumps({
            'response': response
        }))
