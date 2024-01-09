from django.urls import path
from .views import *

urlpatterns = [
    path('', VoteListView.as_view(), name = "home")
]