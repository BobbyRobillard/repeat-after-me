from django.contrib.auth.models import User, AnonymousUser

from django.urls import reverse

from .models import Profile, Settings, Recording
from .utils import (
    get_profiles,
    get_current_profile,
    set_current_profile,
    get_settings,
    toggle_play_mode,
    start_recording,
    stop_recording,
    create_default_testing_profile,
    user1_username,
    user1_password,
)
from .views import DeleteProfileView

from django.test import TestCase, Client, RequestFactory

from rest_framework.authtoken.models import Token


class ProfileTestCase(TestCase):
    def setUp(self):
        self = create_default_testing_profile(self)

        self.other_user = User.objects.create_user(
            username="user2", password=user1_password
        )
        profile2 = Profile.objects.create(name="test2", user=self.user)
        profile3 = Profile.objects.create(name="test3", user=self.other_user)

        Settings.objects.create(
            recording_key="r",
            play_mode_key="p",
            current_profile=profile3,
            user=self.other_user,
        )

    def test_get_profiles(self):
        num_profiles = len(get_profiles(self.user))
        self.assertEqual(num_profiles, 2)

    def test_get_current_profile(self):
        profile = get_current_profile(self.user)
        self.assertEqual(profile.name, "test1")

    def test_set_current_profile(self):
        set_current_profile(self.user, 2)
        current_profile_name = get_current_profile(self.user).name
        self.assertEqual(current_profile_name, "test2")

    def test_set_invalid_current_profile(self):
        self.c.login(username=user1_username, password=user1_password)
        response = self.c.post(reverse("macros:set_current_profile", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 404)

    # Try to delete a user's own profile
    def test_delete_owned_profile(self):
        self.c.login(username=user1_username, password=user1_password)
        profiles = get_profiles(self.user)
        self.assertEqual(len(profiles), 2)

        response = self.c.post(reverse("macros:delete_profile", kwargs={"pk": 1}))
        profiles = get_profiles(self.user)

        # Redirect to homepage
        self.assertEqual(response.status_code, 302)
        # Profile was deleted
        self.assertEqual(len(profiles), 1)
        # New current profile set, since current profile was deleted
        self.assertEqual(get_settings(self.user).current_profile.pk, 2)

    def test_delete_all_profiles(self):
        self.c.login(username=user1_username, password=user1_password)
        response = self.c.post(reverse("macros:delete_profile", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse("macros:delete_profile", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 302)

        # No current profile set, since all were deleted
        self.assertEqual(get_settings(self.user).current_profile, None)
        self.assertEqual(len(get_profiles(self.user)), 0)

    # Try to delete a profile as an anonymous user
    def test_delete_profile_not_logged_in(self):
        response = self.c.post(reverse("macros:delete_profile", kwargs={"pk": 2}))
        profiles = get_profiles(self.user)
        self.assertEqual(len(profiles), 2)

        # Redirected to login
        self.assertEqual(response.status_code, 302)
        # No profile deleted
        self.assertEqual(len(profiles), 2)

    # Try to delete another user's profile
    def test_delete_unowned_profile(self):
        self.c.login(username="user2", password="qzwxec123")
        profiles = get_profiles(self.user)
        self.assertEqual(len(profiles), 2)

        response = self.c.post(reverse("macros:delete_profile", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(profiles), 2)


class SettingsTestCase(TestCase):
    def setUp(self):
        self = create_default_testing_profile(self)
        self.token = Token.objects.create(user=self.user)

    def test_get_settings(self):
        settings = get_settings(self.user)
        self.assertEqual(settings.play_mode, False)
        self.assertEqual(settings.is_recording, False)
        self.assertEqual(settings.offer_tutorial, True)

    def test_toggle_play_mode(self):
        toggle_play_mode(self.token.key, "1")
        settings = get_settings(self.user)
        self.assertEqual(settings.play_mode, True)

        toggle_play_mode(self.token.key, "0")
        settings = get_settings(self.user)
        self.assertEqual(settings.play_mode, False)

    def test_start_recording(self):
        start_recording(self.token.key)
        settings = get_settings(self.user)
        self.assertEqual(settings.is_recording, True)

    def test_stop_recording(self):
        # Make sure system marked user as no longer recording
        stop_recording(self.user)
        settings = get_settings(self.user)
        self.assertEqual(settings.is_recording, False)

    def test_show_social_disable(self):
        self.c.login(username=user1_username, password=user1_password)
        response = self.c.post(reverse("macros:stop_showing_sharing"))
        settings = get_settings(self.user)
        settings.show_social_sharing = False
        settings.save()
        self.assertEqual(settings.show_social_sharing, False)
        self.assertEqual(response.status_code, 302)

    def test_quit_tutorial(self):
        # Tutorial should show by default
        self.c.login(username=user1_username, password=user1_password)
        settings = get_settings(self.user)
        self.assertEqual(settings.offer_tutorial, True)

        response = self.c.post(reverse("macros:quit_tutorial"))
        settings = get_settings(self.user)
        self.assertEqual(settings.offer_tutorial, False)
        self.assertEqual(response.status_code, 302)

    def test_setup_settings(self):
        data = {
            "play_mode_key": "r",
            "recording_key": "a",
            "quick_play_key": "s",
        }
        response = self.c.post(reverse("macros:setup_settings"), data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.settings.play_mode_key, "r")
        self.assertEqual(self.settings.recording_key, "a")
        self.assertEqual(self.settings.quick_play_key, "s")
