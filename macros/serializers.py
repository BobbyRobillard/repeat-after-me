from rest_framework import serializers

from .models import KeyEvent, MouseEvent




class KeyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyEvent
        fields = ["key_code", "delay_time", "is_press"]


class MouseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouseEvent
        fields = ["x_pos", "y_pos", "delay_time", "is_press"]
