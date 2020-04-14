from django.http import JsonResponse, HttpResponse, Http404

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

from rest_framework.authtoken.models import Token

from .models import Profile, Settings, Recording


user1_username = "user1"
user1_password = "qzwxec123"


def name_is_valid(name):
    valid_single_chars = ["-", ",", "_", ".", " ", "'"]
    for char in name:
        if not (char.isalnum() or (char in valid_single_chars)):
            return False
    return True


def user_owners_profile(user, profile_pk):
    return Profile.objects.filter(user=user, pk=profile_pk).exists()


def get_profiles(user):
    return Profile.objects.filter(user=user)


def get_settings(user):
    return Settings.objects.get(user=user)


def get_settings_from_token(token):
    try:
        user = Token.objects.get(key=token).user
    except Exception as e:
        raise Http404

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
        profile=get_current_profile(settings.user), is_temp=True
    ).delete()


def get_current_profile(user):
    return get_settings(user).current_profile


def set_current_profile(user, profile_pk):
    if user_owners_profile(user, profile_pk):
        settings = Settings.objects.get(user=user)
        settings.current_profile = Profile.objects.get(pk=profile_pk)
        settings.save()
    else:
        raise Http404


def set_default_profile(user):
    set_current_profile(user, get_profiles(user).first().pk)


def sync(token):
    settings = get_settings_from_token(token)
    settings.is_recording = False
    settings.play_mode = False
    settings.save()


def get_possible_icons():
    return [
        "fab fa-affiliatetheme",
        "fas fa-adjust",
        "fas fs fa-anchor",
        "fas fa-award",
        "fas fa-book",
        "fas fa-broom",
        "fas fa-bowling-ball",
        "fab fa-blogger",
        "fas fa-bone",
        "fab fa-avianex",
        "fab fa-accessible-icon",
        "fas fa-atom" "fas fa-american-sign-language-interpreting",
        "fab fa-asymmetrik",
        "fas fa-baseball-ball",
        "fas fa-bacon",
        "far fa-bell",
        "fas fa-briefcase-medical",
        "fas fa-burn",
    ]


def create_default_testing_profile(test_object):
    test_object.c = Client()
    test_object.user = User.objects.create_user(
        username=user1_username, password=user1_password
    )
    test_object.profile = Profile.objects.create(name="test1", user=test_object.user)
    test_object.settings = Settings.objects.create(
        recording_key="r",
        play_mode_key="p",
        quick_play_key="a",
        current_profile=test_object.profile,
        user=test_object.user,
    )
    return test_object
