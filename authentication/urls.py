from django.urls import path, include
from .views import *

urlpatterns = [
    path('signin', Login.as_view(), name = "signin"),
    path('signup', Registration.as_view(), name = "signup"),
    path('logout', logout_view, name = "logout"),
]