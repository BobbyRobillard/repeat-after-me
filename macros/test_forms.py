from django.contrib.auth.models import User, AnonymousUser

from . forms import ProfileForm

from django.test import TestCase, Client, RequestFactory


class ProfileFormTests(TestCase):

    def setUp(self):
        self.valid_icon = "fas fa-adjust"
        self.valid_name = "test profile"

    def test_valid_icon_text(self):
        form_data = {'icon': self.valid_icon, 'color': '000000', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_icon_text(self):
        form_data = {'icon': 'abc', 'color': '000000', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': 'fab fa-user', 'color': '000000', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': '#######', 'color': '000000', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data = {'icon': '', 'color': '000000', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_color_data(self):
        form_data = {'icon': self.valid_icon, 'color': '000000', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'icon': self.valid_icon, 'color': '0', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_color_data(self):
        form_data = {'icon': self.valid_icon, 'color': '---', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': self.valid_icon, 'color': '@df676', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': self.valid_icon, 'color': '@df 76', 'name': self.valid_name}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': self.valid_icon, 'color': '7777777', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
