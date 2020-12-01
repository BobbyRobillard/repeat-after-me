from django import forms

from .models import max_name_length, key_code_length, Profile, Settings
from .utils import get_possible_icons, get_settings, name_is_valid


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "color", "icon"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name_is_valid(name):
            raise forms.ValidationError(
                "Names can only contain letters, numbers, spaces, and the following characters - , _ ."
            )
        return name

    def clean_color(self):
        color = self.cleaned_data["color"]
        if not color.isalnum():
            raise forms.ValidationError(
                "Color must be a valid hexidecimal color. Use the selector below if you're expieriencing difficulties"
            )
        return color

    def clean_icon(self):
        icon = self.cleaned_data["icon"].lower()
        if not any(icon == valid_icon for valid_icon in get_possible_icons()):
            raise forms.ValidationError("That is not a valid icon option.")

        return icon


class RecordingForm(forms.Form):
    name = forms.CharField(max_length=max_name_length,
                           widget=forms.TextInput(attrs={'placeholder':'Recording Name...'}))
    key_code = forms.CharField(max_length=key_code_length, widget=forms.TextInput(attrs={'placeholder':'Activation Key Code...'}))

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name_is_valid(name):
            raise forms.ValidationError(
                "Names can only contain letters, numbers, spaces, and the following characters - , _ ."
            )
        return name

    def clean_key_code(self):
        key_code = self.cleaned_data["key_code"]
        settings = get_settings(self.user)

        if key_code == settings.play_mode_key:
            raise forms.ValidationError(
                'Your Play Mode Key is bound to "{0}", please select another key!'.format(
                    key_code
                )
            )

        if key_code == settings.recording_key:
            raise forms.ValidationError(
                'Your Recording Key is bound to "{0}", please select another key!'.format(
                    key_code
                )
            )

        return key_code


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ["play_mode_key", "recording_key", "quick_play_key"]

    def clean(self):
        data = self.cleaned_data
        play_mode_key = self.cleaned_data["play_mode_key"]
        recording_key = self.cleaned_data["recording_key"]
        quick_play_key = self.cleaned_data["quick_play_key"]
        if play_mode_key == recording_key:
            raise forms.ValidationError(
                {"play_mode_key": "Play Mode Key can't be the same as your Recording Key"}
            )
        if quick_play_key == recording_key:
            raise forms.ValidationError(
                {"quick_play_key": "Quick Play Key can't be the same as your Recording Key"}
            )
        if quick_play_key == play_mode_key:
            raise forms.ValidationError(
                {"quick_play_key": "Quick Play Key can't be the same as your Play Mode Key"}
            )
        return data
