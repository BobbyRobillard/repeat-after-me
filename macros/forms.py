from django import forms

from .models import Profile, max_name_length


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=max_name_length)
