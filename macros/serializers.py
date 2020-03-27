from rest_framework import serializers

from .models import KeyEvent, MouseEvent


class KeyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyEvent
        fields = ["key_code", "delay_time", "is_press", "order_in_recording"]


class MouseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouseEvent
        fields = ["x_pos", "y_pos", "delay_time", "is_press", "order_in_recording"]
