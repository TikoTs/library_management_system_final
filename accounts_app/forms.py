from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from accounts_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, help_text='Required. Enter your full name.')
    personal_number = forms.CharField(max_length=20, required=True, help_text='Required. Enter your personal number.')
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}),
                                 help_text='Required. Enter your birth date.')

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'full_name', 'personal_number', 'birth_date', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'full_name', 'personal_number', 'birth_date', 'is_staff', 'is_active', 'groups',
            'user_permissions')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, help_text='Required. Enter a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Required. Enter your password.')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")
        return email


