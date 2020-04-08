from django.urls import reverse

from django.test import TestCase, Client


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
        data['username'] = 'test1'
        data['password1'] = ''
        response = self.c.post(reverse("core:register"), data)
        self.assertEqual(response.status_code, 200)
