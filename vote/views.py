from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.utils import timezone

# Create your views here.
class VoteListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = super().get_queryset() 
        now = timezone.now()
        context['expired'] = qs.filter(end_time__lte = now)
        context['current'] = qs.filter(end_time__gte = now)
        return context


class VoteDetailView(DetailView):
    model = Voting
    template_name = 'votings/voting_detail.html'
    context_object_name = 'voting'