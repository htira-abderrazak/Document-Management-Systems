
# user/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.user_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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
