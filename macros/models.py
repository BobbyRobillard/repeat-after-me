from django.db import models
from django.conf import settings
from django.contrib.auth.models import User as User


max_name_length = 75
key_code_length = 10


class Profile(models.Model):
    def __str__(self):
        return self.name

    def get_recordings(self):
        return Recording.objects.filter(profile=self)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=max_name_length)
    color = models.CharField(max_length=6)
    icon = models.CharField(max_length=30, default="fas fa-user")


class Settings(models.Model):
    def __str__(self):
        return "{0}: settings".format(str(self.user))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    auth_token = models.CharField(max_length=150, null=True)
    recording_key = models.CharField(max_length=key_code_length)
    play_mode_key = models.CharField(max_length=key_code_length)
    play_mode = models.BooleanField(default=False)
    is_recording = models.BooleanField(default=False)
    offer_tutorial = models.BooleanField(default=True)
    current_profile = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True)


class Recording(models.Model):
    def __str__(self):
        return "{0} | {1}".format(str(self.profile), self.name)

    def get_events(self):
        return {
            "key_events": KeyEvent.objects.filter(recording=self),
            "mouse_events": MouseEvent.objects.filter(recording=self),
        }

    name = models.CharField(max_length=max_name_length)
    key_code = models.CharField(max_length=key_code_length, null=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    is_temp = models.BooleanField(default=False)


class MouseEvent(models.Model):
    def __str__(self):
        return "{0} - Mouse Event ({1}, {2})".format(
            self.recording.name, self.x_pos, self.y_pos
        )

    x_pos = models.IntegerField(default=0)
    y_pos = models.IntegerField(default=0)
    delay_time = models.IntegerField(default=0)
    is_press = models.BooleanField(default=True)
    recording = models.ForeignKey("Recording", on_delete=models.CASCADE)
    order_in_recording = models.IntegerField(default=(-1))


class KeyEvent(models.Model):
    def __str__(self):
        return "{0} - Key Event ({1})".format(self.recording.name, self.key_code)

    key_code = models.CharField(max_length=key_code_length)
    delay_time = models.IntegerField(default=0)
    is_press = models.BooleanField(default=True)
    recording = models.ForeignKey("Recording", on_delete=models.CASCADE)
    order_in_recording = models.IntegerField(default=(-1))
