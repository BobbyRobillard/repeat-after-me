from django import forms

from .models import max_name_length, key_code_length, Profile
from .utils import get_possible_icons, get_settings, name_is_valid


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'color', 'icon']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name_is_valid(name):
            raise forms.ValidationError("Names can only contain letters, numbers, spaces, and the following characters - , _ .")
        return name

    def clean_color(self):
        color = self.cleaned_data["color"]
        if not color.isalnum():
            raise forms.ValidationError("Color must be a valid hexidecimal color. Use the selector below if you're expieriencing difficulties")
        return color

    def clean_icon(self):
        icon = self.cleaned_data['icon'].lower()
        if not any(icon == valid_icon for valid_icon in get_possible_icons()):
            raise forms.ValidationError("That is not a valid icon option.")

        return icon


class RecordingForm(forms.Form):
    name = forms.CharField(max_length=max_name_length)
    key_code = forms.CharField(max_length=key_code_length)

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name_is_valid(name):
            raise forms.ValidationError("Names can only contain letters, numbers, spaces, and the following characters - , _ .")
        return name

    def clean_key_code(self):
        key_code = self.cleaned_data['key_code']
        settings = get_settings(self.user)

        if key_code == settings.play_mode_key:
            raise forms.ValidationError("Your Play Mode Key is bound to \"{0}\", please select another key!".format(
                key_code
            ))

        if key_code == settings.recording_key:
            raise forms.ValidationError("Your Recording Key is bound to \"{0}\", please select another key!".format(
                key_code
            ))

        return key_code


class SettingsForm(forms.Form):
    play_key = forms.CharField(max_length=10)
    recording_key = forms.CharField(max_length=10)
