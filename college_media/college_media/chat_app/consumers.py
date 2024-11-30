import json
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from django.contrib.auth import get_user_model
from .models import  Message,Notification
from staff_app .models import CoustomUser
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async # type: ignore
User = get_user_model()
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Room name is based on the conversation ID
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.sender = self.scope['user']
        self.room_group_name = f'chat_{min(self.sender.id, int(self.receiver_id))}_{max(self.sender.id, int(self.receiver_id))}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self,close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        timestamp=data['timestamp']
        print(timestamp)
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = timestamp.strftime('%b. %d, %Y, %I:%M %p').lower().replace('am', 'a.m.').replace('pm', 'p.m.')

        # Save message to the database
        sender =await sync_to_async( CoustomUser.objects.get)(id=self.sender.id)
        receiver = await sync_to_async(CoustomUser.objects.get)(id=self.receiver_id)
        print(self.receiver_id)
        await database_sync_to_async(Message.objects.create)(
             sender=sender,receiver=receiver ,content=message
        )
        await database_sync_to_async(Notification.objects.create)(sender=sender,receiver=receiver,content=message,)
        print("__Object is createdc")


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.id,
                'timestamp' : timestamp
            }
        )
        await self.channel_layer.group_send(
            f'notificatio_{receiver.id}',  # This is the room for notifications
            {
                'type': 'send_notification',
                'unread': await self.get_unread_notifications(receiver.id)  # Get unread notification count
            }
        )   
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp=event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp':timestamp
        }))
    @sync_to_async
    def get_unread_notifications(self, user_id):
        return Notification.objects.filter(receiver_id=user_id, is_read=False).count()
        
class Notifications(AsyncWebsocketConsumer):
    # Room name is based on the conversation ID
    async def connect(self):
        # self.receiver_id=self.scope['url_route']['kwargs']['receiver_id']
        self.sender=self.scope['user']
        if self.sender.is_authenticated:
            self.room_group_name = f'notificatio_{self.sender.id}'
            # print("--------------------------------------------")
            # print("Reciver:{} Sender : {} room:{}".format(self.receiver_id,self.sender,self.room_group_name))
            
            await self.channel_layer.group_add(self.room_group_name,self.channel_name)
            await self.accept()
            unread=await sync_to_async(Notification.objects.filter(receiver=self.sender, is_read=False).count)()
            print("__________UNREAD_COUNT____________")
            print(unread)
            await self.send(text_data=json.dumps({
                'new_notifications':True,
                'unread':unread
            }))
        else:
            await self.close()
        # unread= await sync_to_async(Notification.objects.filter)(receiver=self.sender,is_read=False).count()
    async def disconnect(self, *args, **kwargs):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
    
    async def receive(self):
        # For future extensions if needed
        pass
    async  def send_notification(self,event): 
        unread=await sync_to_async(Notification.objects.filter(receiver=self.sender, is_read=False).count)()
        await self.send(text_data=json.dumps({
                'new_notifications':True,
                'unread':unread
            }))
    #     data = json.loads(text_data)
    #     sender_id=data['sender_id']
    #     message=data['message']
    #     receiver_id=data['reciver_id']
    #     timestamp=data['timestamp']
        
    #     timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    #     timestamp = timestamp.strftime('%b. %d, %Y, %I:%M %p').lower().replace('am', 'a.m.').replace('pm', 'p.m.')
    #     sender =await sync_to_async( CoustomUser.objects.get)(id=self.sender.id)
    #     receiver = await sync_to_async(CoustomUser.objects.get)(id=self.receiver_id)
    #     await database_sync_to_async(Notification.objects.create)(sender=sender,receiver=receiver,content=message,)
    #     print("__Object is createdc")
    #     print("---------- Sender Information--------------")
    #     print(sender_id)
    #     print(message)
    #     print(receiver_id)
    #     print(timestamp)
    #     print("-----------------------------------------------")
        