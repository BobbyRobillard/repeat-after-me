from django.contrib.auth.models import User, AnonymousUser

from . forms import ProfileForm

from django.test import TestCase, Client, RequestFactory


class ProfileFormTests(TestCase):
    def test_valid_form_data(self):
        form_data = {'color': '000000', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'color': '0', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        form_data = {'color': '---', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'color': '@df676', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'color': '@df 76', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'color': '7777777', 'name': 'test profile'}
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
