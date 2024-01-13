from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.utils import timezone
from django.http import JsonResponse


class FinishedVotingsListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'

    def get_queryset(self) -> QuerySet[Any]:
        return Voting.objects.filter(end_time__lte = timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Finished votings"
        return context

class CurrentVotingsListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'

    def get_queryset(self) -> QuerySet[Any]:
        now = timezone.now()
        return Voting.objects.filter(end_time__gte = now, start_time__lte = now)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Current votings"
        return context


class UpcomingVotingsListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'

    def get_queryset(self) -> QuerySet[Any]:
        return Voting.objects.filter(start_time__gte = timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Upcoming votings"
        return context



class VoteDetailView(DetailView):
    model = Voting
    template_name = 'votings/voting_detail.html'
    context_object_name = 'voting'    context_object_name = 'voting'
