from django.shortcuts import render
from django.views.generic import ListView
from .models import *

# Create your views here.
class VoteListView(ListView):
    model = Vote
    template_name = 'votes/vote_list.html'
    context_object_name = 'votes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = super().get_queryset() 
        context['expired'] = qs.filter(expired = True)
        context['current'] = qs.filter(expired = False)
        return context