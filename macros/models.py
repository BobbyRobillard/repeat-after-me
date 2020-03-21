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


class Settings(models.Model):
    def __str__(self):
        return "{0}: settings".format(str(self.user))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    recording_key = models.CharField(max_length=key_code_length)
    play_mode_key = models.CharField(max_length=key_code_length)
    play_mode = models.BooleanField(default=False)
    updates_waiting = models.BooleanField(default=False)
    current_profile = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)


class Recording(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=max_name_length)
    key_code = models.CharField(max_length=key_code_length)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class MouseEvent(models.Model):
    def __str__(self):
        return "{0} - Mouse Event ({1}, {2})".format(
            self.recording.name, self.x_pos, self.y_pos
        )

    x_pos = models.IntegerField()
    y_pos = models.IntegerField()
    delay_time = models.IntegerField(default=0)
    is_press = models.BooleanField()
    recording = models.ForeignKey('Recording', on_delete=models.CASCADE)


class KeyEvent(models.Model):
    def __str__(self):
        return "{0} - Key Event ({1})".format(self.recording.name, self.key_code)

    key_code = models.CharField(max_length=key_code_length)
    delay_time = models.IntegerField(default=0)
    is_press = models.BooleanField()
    recording = models.ForeignKey('Recording', on_delete=models.CASCADE)
