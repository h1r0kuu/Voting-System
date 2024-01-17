from django.urls import path
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name = "login"),
    path('signup', Registration.as_view(), name = "signup"),
    path('settings', UserChangeSettingsView.as_view(), name = "settings"),
    path('logout', logout_view, name = "logout")
]