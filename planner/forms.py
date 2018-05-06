from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput


class ReportChangeForm(forms.Form):
    change_start_date = forms.DateField()
    change_end_date = forms.DateField()

    new_start_time = forms.TimeField()
    new_end_time = forms.TimeField()

    new_day_of_week = forms.IntegerField()

    one_time_change = forms.BooleanField()


# Custom fields (i.e. placeholders) in several forms:

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=EmailInput(attrs={'class': 'validate', 'placeholder': 'Email'}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Repeat password'}))
