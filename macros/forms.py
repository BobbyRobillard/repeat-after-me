from django import forms

from .models import max_name_length, key_code_length, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'color']

    def clean_color(self):
        color = self.cleaned_data["color"]
        if not color.isalnum():
            raise forms.ValidationError("Color must be a valid Hexidecimal color code. Use the selector below if you're expieriencing difficulties")
        return color


class RecordingForm(forms.Form):
    name = forms.CharField(max_length=max_name_length)
    key_code = forms.CharField(max_length=key_code_length)
