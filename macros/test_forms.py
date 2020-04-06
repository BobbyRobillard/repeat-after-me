from django.contrib.auth.models import User, AnonymousUser

from . forms import ProfileForm

from django.test import TestCase, Client, RequestFactory


class ProfileFormTests(TestCase):
    def test_valid_icon_text(self):
        form_data = {'icon': 'fas fa-user', 'color': '000000', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_icon_text(self):
        form_data = {'icon': 'fas fa-user', 'color': '000000', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'icon': 'fas fa-user', 'color': '0', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_color_data(self):
        form_data = {'icon': 'fas fa-user', 'color': '000000', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'icon': 'fas fa-user', 'color': '0', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_color_data(self):
        form_data = {'icon': 'fas fa-user', 'color': '---', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': 'fas fa-user', 'color': '@df676', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': 'fas fa-user', 'color': '@df 76', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'icon': 'fas fa-user', 'color': '7777777', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
