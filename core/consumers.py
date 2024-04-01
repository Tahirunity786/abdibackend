from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        cookies = self.scope['cookies']
        session_id = cookies.get('sessionid', '')
        user = await self.authenticate_user(session_id)
        
        if user is None:
            await self.close()
        else:
            self.user = user
            self.group_name = f'user_{user.id}_notifications'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()


    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )


    async def send_notification(self, event):
        message = event.get('message')
        print(message)
        if message:
            await self.send(text_data=message)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    async def authenticate_user(self, session_id):
        session_data = await self.get_session_data(session_id)
        user_id = session_data.get('_auth_user_id')
        
        if user_id is not None:
            return await self.get_user(user_id)
        
        return None
    
    @database_sync_to_async
    def get_session_data(self, session_id):
        from django.contrib.sessions.models import Session
        try:
            session = Session.objects.get(session_key=session_id)
            return session.get_decoded()
        except Session.DoesNotExist:
            return {}