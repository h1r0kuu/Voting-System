from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name = "login"),
    path("", include('django.contrib.auth.urls'))
]