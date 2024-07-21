import datetime
import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from .models import Message
import json
import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User
import datetime
class PersonalChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chat_name = self.scope['url_route']['kwargs']['user_name']
        self.chat = User.objects.filter(username=self.chat_name).first()

        if self.chat:
            async_to_sync(self.channel_layer.group_add)(
                f"user_{self.user.username}",
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave the channel group
        async_to_sync(self.channel_layer.group_discard)(
            f"user_{self.user.username}",
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('message'):
            message = text_data_json.get('message')
        else:
            message=''
        receiver_username = text_data_json.get('receiver')
        image_data = text_data_json.get('image')  # Handle image data

        time = datetime.datetime.now().strftime('%d/%m/%Y, %I:%M:%S %p')

        if not receiver_username:
            return

        receiver = User.objects.filter(username=receiver_username).first()
        if not receiver:
            print('Receiver does not exist')
            return

        # Handle image data if present
        if image_data:
            try:
                # Decode the base64 data
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = base64.b64decode(imgstr)
                image_file = ContentFile(data, name=f'{self.user.username}_image.{ext}')

                # Create the message with image
                message_obj = Message.objects.create(
                    sender=self.user,
                    receiver=receiver,
                    content=message,
                    media_image=image_file,
                    timestamp=datetime.datetime.now(),
                )
            except Exception as e:
                print(f"Error handling image: {e}")
                return
        else:
            # Create message with text content only
            message_obj = Message.objects.create(
                sender=self.user,
                receiver=receiver,
                content=message,
                timestamp=datetime.datetime.now(),
            )

        try:
            async_to_sync(self.channel_layer.group_send)(
                f"user_{receiver_username}",
                {
                    'type': 'chat_message',
                    'message': message,
                    'image':image_data,
                    'sender': self.user.username,
                    'time': time
                }
            )
        except Exception as e:
            print(f"Error sending message: {e}")
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        time=event['time']
        image_data=event['image']

        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'image': image_data,
            'time': time
        }))
