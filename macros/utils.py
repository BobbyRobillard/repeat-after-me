from .models import Profile, Settings


def get_profiles(user):
    return Profile.objects.filter(user=user)


def get_current_profile(user):
    return Settings.objects.get(user=user).current_profile
