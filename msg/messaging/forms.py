from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from .models import Profile
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control custom-username', 'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control custom-email', 'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control custom-password1', 'placeholder': 'Enter Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control custom-password2', 'placeholder': 'Confirm Password'})

        # Remove default help texts
        self.fields['username'].help_text=None
        self.fields['email'].help_text=None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'bio']