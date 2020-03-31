from django import forms

from .models import max_name_length, key_code_length


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=max_name_length)
    color = forms.CharField(max_length=7)

    def clean_color(self):
        color = self.cleaned_data['color']
        return color.replace('#', '')


class RecordingForm(forms.Form):
    name = forms.CharField(max_length=max_name_length)
    key_code = forms.CharField(max_length=key_code_length)
