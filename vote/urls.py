from django.urls import path
from .views import *

urlpatterns = [
    path('', CurrentVotingsListView.as_view(), name = "home"),
    path('vote/<int:pk>', VoteDetailView.as_view(), name = "vote_details"),
    path('votings/upcoming', UpcomingVotingsListView.as_view(), name = 'upcoming_votings'),
    path('votings/current', CurrentVotingsListView.as_view(), name = 'current_votings'),
    path('votings/finished', FinishedVotingsListView.as_view(), name = 'finished_votings'),
    path('voting/get_options', GetOptionsView.as_view(), name='get_voting_options'),

]