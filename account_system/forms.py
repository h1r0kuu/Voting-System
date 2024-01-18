from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
import re


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs = {
        'class': 'form-control'
    }), label = "Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class': 'form-control'
    }))

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs = {
        'class': 'form-control'
    }), label = "Username", min_length = 5, max_length = 20)
    email = forms.CharField(widget=forms.EmailInput(attrs = {
        'class': 'form-control'
    }), label = "Email")
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class': 'form-control'
    }))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', )

class ChangeSettingsForm(UserChangeForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs = {
        'class': 'form-control'
    }), label = "Username", min_length = 5, max_length = 20)
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs = {
        'class': 'form-control'
    }), label = "First name", min_length = 5, max_length = 20)
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs = {
        'class': 'form-control'
    }), label = "Last name", min_length = 5, max_length = 20)
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs = {
        'class': 'form-control'
    }), label = "Email")

    password = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email' )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.match(r'^[a-zA-Z]+$', first_name):
            raise forms.ValidationError('First name can only contain letters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-Z]+$', last_name):
            raise forms.ValidationError('Last name can only contain letters.')
        return last_name

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class': 'form-control'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class': 'form-control'
    }), label = "New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class': 'form-control'
    }), label = "Confirm new password")

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password1')
    
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        print("here")
        if not self.user.check_password(old_password):
            raise forms.ValidationError({'old_password': 'Old password is not correct'})
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError({'new_password2': 'Passwords do not match'})