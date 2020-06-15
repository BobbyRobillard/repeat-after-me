import json
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

from .utils import get_settings


class PlayConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        settings = get_settings(self.scope["user"])
        self.send(
            text_data=json.dumps(
                {"playMode": settings.play_mode, "isRecording": settings.is_recording}
            )
        )

    # def connect(self):
    #     async_to_sync(self.channel_layer.group_add)("test", self.channel_name)
    #
    # def disconnect(self, close_code):
    #     async_to_sync(self.channel_layer.group_discard)("test", self.channel_name)
    #
    # def update_settings(self, event):
    #     settings = get_settings(self.scope['user'])
    #     self.send(text_data=json.dumps(
    #         {
    #             "playMode": settings.play_mode,
    #             "isRecording": settings.is_recording
    #         }
    #     ))
