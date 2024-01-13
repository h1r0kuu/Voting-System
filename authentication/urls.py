from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name = "login"),
    path('signup', Registration.as_view(), name = "signup"),
    path('logout', logout_view, name = "logout"),
]