from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class TestConsumer(WebsocketConsumer):

    # called when a connect request is sent to this socket
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        # self.send is always used to send data from backend to frontend.
        self.send(text_data=json.dumps({"status": "connected from django channels"}))

    # used to receive data from frontend
    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps(text_data))

    # called when socket is closed
    def disconnect(self, *args, **kwargs):
        print("disconnected")

    # created for the def save() function in Notification model.
    def send_notification(self, event):
        data = json.loads(event.get("value"))
        self.send(text_data=json.dumps({"payload": data}))
