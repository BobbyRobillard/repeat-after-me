from django.urls import reverse

from django.contrib.auth.models import User

from django.test import TestCase, Client

from macros.utils import get_settings


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_valid_registration(self):
        data = {
            "username": "test",
            "email": "test@techandmech.com",
            "password1": "test321!@#test",
            "password2": "test321!@#test",
            "first_name": "John",
            "last_name": "Mc. Test",
        }
        response = self.c.post(reverse("core:register"), data)
        # Redirected to homepage on sucessful signup
        self.assertEqual(response.status_code, 302)

        settings = get_settings(User.objects.get(username="test"))

        # Make sure settings were created with the proper default values
        self.assertTrue(settings is not None)
        self.assertEqual(settings.recording_key, "r")
        self.assertEqual(settings.play_mode_key, "p")
        self.assertEqual(settings.quick_play_key, "a")

    def test_invalid_registration(self):
        data = {
            "username": "test",
            "email": "test@techandmech.com",
            "password1": "test321!@#test",
            "password2": "test321!@#test",
            "first_name": "John",
            "last_name": "Mc. Test",
        }
        # Duplicate user
        response = self.c.post(reverse("core:register"), data)
        response = self.c.post(reverse("core:register"), data)
        # The signup page should be re-rendered, because of errors
        self.assertEqual(response.status_code, 200)

        # No Password1
        data["password1"] = ""
        response = self.c.post(reverse("core:register"), data)
        self.assertEqual(response.status_code, 200)
