from django.contrib.auth.models import User as User

from .models import Profile, Settings, Recording

from rest_framework.authtoken.models import Token


def user_owners_profile(user, profile_pk):
    return Profile.objects.filter(user=user, pk=profile_pk).exists()


def get_profiles(user):
    return Profile.objects.filter(user=user)


def get_settings(user):
    return Settings.objects.get(user=user)


def get_settings_from_token(token):
    user = Token.objects.get(key=token).user
    settings = get_settings(user)
    return settings


def toggle_play_mode(token, toggle):
    settings = get_settings_from_token(token)

    if toggle == "0":
        settings.play_mode = False
    elif toggle == "1":
        settings.play_mode = True

    settings.save()


def stop_recording(user):
    settings = get_settings(user)
    settings.is_recording = False
    settings.save()


def start_recording(token):
    settings = get_settings_from_token(token)
    settings.is_recording = True
    settings.save()

    # Delete any previous temporary recordings
    Recording.objects.filter(
        profile=get_current_profile(settings.user), 
        is_temp=True
    ).delete()


def get_current_profile(user):
    return get_settings(user).current_profile


def set_current_profile(user, profile_pk):
    if user_owners_profile(user, profile_pk):
        user_settings = Settings.objects.get(user=user)
        user_settings.current_profile = Profile.objects.get(pk=profile_pk)
        user_settings.save()
        return True
    return False


def set_default_profile(user):
    set_current_profile(user, get_profiles(user).first().pk)


def sync(token):
    settings = get_settings_from_token(token)
    settings.is_recording = False
    settings.play_mode = False
    settings.save()
