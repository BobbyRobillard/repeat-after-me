from django.contrib.auth.models import User, AnonymousUser

from .models import Settings
from .forms import ProfileForm, RecordingForm, SettingsForm

from django.test import TestCase, Client, RequestFactory


class SettingsFormTests(TestCase):
    def test_valid_settings(self):
        form_data = {"play_key": "p", "recording_key": "r"}
        form = SettingsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_settings(self):
        form_data = {"play_key": "a", "recording_key": "a"}
        form = SettingsForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProfileFormTests(TestCase):
    def setUp(self):
        self.valid_icon = "fas fa-adjust"
        self.valid_name = "test profile"
        self.valid_color = "000000"

    def test_valid_icon_text(self):
        form_data = {
            "icon": self.valid_icon,
            "color": self.valid_color,
            "name": self.valid_name,
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_icon_text(self):
        form_data = {"icon": "abc", "color": self.valid_color, "name": self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "icon": "fab fa-user",
            "color": self.valid_color,
            "name": self.valid_name,
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "icon": "#######",
            "color": self.valid_color,
            "name": self.valid_name,
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {"icon": "", "color": "000000", "name": self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_color_data(self):
        form_data = {
            "icon": self.valid_icon,
            "color": self.valid_color,
            "name": self.valid_name,
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"icon": self.valid_icon, "color": "0", "name": self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_color_data(self):
        form_data = {"icon": self.valid_icon, "color": "---", "name": self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "icon": self.valid_icon,
            "color": "@df676",
            "name": self.valid_name,
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "icon": self.valid_icon,
            "color": "@df 76",
            "name": self.valid_name,
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "icon": self.valid_icon,
            "color": "7777777",
            "name": "test profile",
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {"icon": self.valid_icon, "color": "", "name": "test profile"}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_name(self):
        valid_names = [
            "james",
            "james whitten",
            "james_whitten",
            "james-whitten",
            "whitten's favorites",
            "james and, whitten",
            "james.whitten",
        ]

        for name in valid_names:
            form_data = {
                "icon": self.valid_icon,
                "color": self.valid_color,
                "name": name,
            }
            form = ProfileForm(data=form_data)
            self.assertTrue(form.is_valid())

    def test_valid_name(self):
        invalid_names = [
            "",
            "@james",
            "/",
            "\\",
            "©",
            "+",
            "=",
            "`",
            "~",
            "<",
            ">",
            "?",
            "|",
            "*",
            "tom!",
            "mary[",
            "[",
            "]",
            ")",
            "(",
        ]
        for name in invalid_names:
            form_data = {
                "icon": self.valid_icon,
                "color": self.valid_color,
                "name": name,
            }
            form = ProfileForm(data=form_data)
            self.assertFalse(form.is_valid())


class RecordingFormTests(TestCase):
    def setUp(self):
        self.valid_name = "test recording"
        self.user = User.objects.create_user(username="user1", password="qzwxec123")

        Settings.objects.create(recording_key="r", play_mode_key="p", user=self.user)

    def test_valid_recording_key(self):
        for valid_key in ["a", "1", "@"]:
            form_data = {"key_code": valid_key, "name": self.valid_name}
            form = RecordingForm(data=form_data)
            # need to set this because of how to code works in the form
            form.user = self.user
            self.assertTrue(form.is_valid())

    def test_invalid_recording_key(self):
        for invalid_key in ["r", "p"]:
            form_data = {"key_code": invalid_key, "name": self.valid_name}
            form = RecordingForm(data=form_data)
            # need to set this because of how to code works in the form
            form.user = self.user
            self.assertFalse(form.is_valid())
