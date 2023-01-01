import json
from asgiref.sync import sync_to_async
from channels.consumer import SyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.accounts.models import User
from apps.chats.models import ChatModel


class PersonalChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        me = self.scope['user'].username
        other_username = self.scope['url_route']['kwargs']['username']
        if len(me) > len(other_username):
            self.room_name = f"{me}-{other_username}"
        else:
            self.room_name = f"{other_username}-{me}"
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        # await self.send(text_data=self.room_group_name)

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer,
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        sender = await sync_to_async(User.objects.get, thread_sensitive=True)(username=username)

        await self.save_message(sender, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        ChatModel.objects.create(
            msg_sender=username,
            message=message,
            thread_name=thread_name
        )


# class EchoConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print("Connect event is called")
#         self.send({
#             'type': 'websocket.accept'
#         })
#
#     def websocket_recieve(self, event):
#         print(event)
#         self.send({
#             'type': 'websocket.send',
#             'text': event.get('text')
#         })
#
#     def websocket_disconnect(self, event):
#         print("Connection is disconnected")
#         print(event)
