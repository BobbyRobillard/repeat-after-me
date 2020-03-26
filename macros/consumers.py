import json
from channels.generic.websocket import WebsocketConsumer

from .utils import get_settings

class PlayConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'playMode': get_settings(self.scope["user"]).play_mode
        }))
