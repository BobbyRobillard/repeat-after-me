from .models import Profile, Settings


def user_owners_profile(user, profile_pk):
    return Profile.objects.filter(user=user, pk=profile_pk).exists()


def get_profiles(user):
    return Profile.objects.filter(user=user)


def get_current_profile(user):
    return Settings.objects.get(user=user).current_profile


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
