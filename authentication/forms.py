from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from vote.models import User

class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs = {
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs = {
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs = {
                'class': 'form-control'
            }),
            'password2': forms.PasswordInput(attrs = {
                'class': 'form-control'
            }),
        }