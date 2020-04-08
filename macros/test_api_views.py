from django.contrib.auth.models import User, AnonymousUser

from django.test import TestCase, Client, RequestFactory

from django.urls import reverse

from rest_framework.authtoken.models import Token

from .models import Settings, Profile

from .utils import create_default_testing_profile, user1_username, user1_password


class TestAPI_General(TestCase):
    def setUp(self):
        self = create_default_testing_profile(self)
        self.c.login(username=user1_username, password=user1_password)
        response = self.c.get(reverse("macros:generate_token"))
        # Successful generation
        self.assertEqual(response.status_code, 200)

        self.token = Token.objects.get(user=self.user)

    def test_invalid_token(self):
        response = self.c.get(
            reverse("macros:start_recording", kwargs={"token": "abc123"})
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_token(self):
        response = self.c.get(
            reverse("macros:start_recording", kwargs={"token": self.token})
        )
        self.assertEqual(response.status_code, 200)
