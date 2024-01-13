from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

# Create your views here.
class Login(View):
    form_class = SignInForm
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
            group, created = Group.objects.get_or_create(name='użytkownik')
            user.groups.add(group)
        return redirect("home")
        
def logout_view(request):
    logout(request)
    return redirect("home")