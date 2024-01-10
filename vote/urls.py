from django.urls import path
from .views import *

urlpatterns = [
    path('', VoteListView.as_view(), name = "home"),
    path('vote/<int:pk>', VoteDetailView.as_view(), name = "vote_details")
]