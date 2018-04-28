from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput


"""This file provides a way to customize forms (i.e. add placeholders)"""

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
    # email = forms.CharField(widget=EmailInput(attrs={'class': 'validate', 'placeholder': 'Email'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=EmailInput(attrs={'class': 'validate', 'placeholder': 'Email'}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Repeat password'}))
