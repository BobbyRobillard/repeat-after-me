from django.contrib.auth.models import User as User

from .models import Profile, Settings, Recording

from rest_framework.authtoken.models import Token


def user_owners_profile(user, profile_pk):
    return Profile.objects.filter(user=user, pk=profile_pk).exists()


def get_profiles(user):
    return Profile.objects.filter(user=user)


def get_settings(user):
    return Settings.objects.get(user=user)


def updates_needed(user):
    settings = get_settings(user)
    settings.updates_needed = True
    settings.save()


def toggle_play_mode(token, toggle):
    user = Token.objects.get(key=token).user
    settings = get_settings(user)

    if toggle == "0":
        settings.play_mode = False
    elif toggle == "1":
        settings.play_mode = True

    settings.save()
    updates_needed(user)


def stop_recording(user):
    settings = get_settings(user)
    settings.is_recording = False
    settings.save()


def start_recording(token):
    user = Token.objects.get(key=token).user
    settings = get_settings(user)
    settings.is_recording = True
    settings.save()

    # Delete any previous temporary recordings
    Recording.objects.filter(
        profile=get_current_profile(user),
        is_temp=True
    ).delete()


def get_current_profile(user):
    return get_settings(user).current_profile


def delete_profile(user, profile_pk):
    if user_owners_profile(user, profile_pk):
        Profile.objects.get(pk=profile_pk).delete()
        set_default_profile(user)
        return True
    return False


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
    user = Token.objects.get(key=token).user
    settings = get_settings(user)
    settings.is_recording = False
    settings.play_mode = False
    settings.save()
