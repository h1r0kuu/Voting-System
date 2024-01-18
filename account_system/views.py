from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash


class Login(View):
    form_class = LoginForm
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")


class Registration(View):
    form_class = SignUpForm
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():     
            user = form.save()
            group, _ = Group.objects.get_or_create(name='użytkownik')
            user.groups.add(group)
        return redirect("home")
        

class UserChangeSettingsView(View):
    general_form_class = ChangeSettingsForm
    password_form_class = ChangePasswordForm
    general_form_button_name = "change_general"
    password_button_name = "change_password"

    template_name = "settings.html"

    def get_context_data(self, request, **kwargs):
        context = {
            'general_form': self.general_form_class(instance = request.user),
            'password_form': self.password_form_class(user = request.user),

            'general_form_button': self.general_form_button_name,
            'password_form_button': self.password_button_name,
        }
        return context
    
    def get_invalid_form_context_data(self, general_form, password_form):
        context = {
            'general_form': general_form,
            'password_form': password_form,

            'general_form_button': self.general_form_button_name,
            'password_form_button': self.password_button_name,
        }
        return context
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        if self.general_form_button_name in request.POST:
            general_form = self.general_form_class(request.POST, instance=request.user)
            if general_form.is_valid():     
                general_form.save()
                messages.success(request, "Ustawienia ogólne zostały zaktualizowane!")
            else:
                messages.error(request, "Coś poszło nie tak :(")
                return render(request, self.template_name, context=self.get_invalid_form_context_data(general_form, self.password_form_class(user = request.user)))
        elif self.password_button_name in request.POST:
            password_form = self.password_form_class(data=request.POST, user=request.user)
            if password_form.is_valid():     
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Hasło zostało zmienione!")
            else:
                messages.error(request, "Coś poszło nie tak :(")
                return render(request, self.template_name, context=self.get_invalid_form_context_data(self.general_form_class(instance = request.user), password_form))
        return render(request, self.template_name, context=self.get_context_data(request))


def logout_view(request):
    logout(request)
    return redirect("home")