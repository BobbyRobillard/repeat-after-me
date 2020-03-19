from .models import Profile


def get_profiles(user):
    return Profile.objects.filter(user=user)
