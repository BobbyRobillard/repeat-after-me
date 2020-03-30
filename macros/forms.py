from django import forms

from .models import Profile, max_name_length


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=max_name_length)
    color = forms.CharField(max_length=7)

    def clean_color(self):
        color = self.cleaned_data['color']
        return color.replace('#', '')
