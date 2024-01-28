from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from .models import *
from django.utils import timezone
from django.http import JsonResponse


class FinishedVotingsListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Voting.objects.filter(end_time__lte = timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Zakończone głosowania"
        return context

class CurrentVotingsListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        now = timezone.now()
        return Voting.objects.filter(end_time__gte = now, start_time__lte = now, open_for_voting = True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Aktualne głosowania"
        return context


class UpcomingVotingsListView(ListView):
    model = Voting
    template_name = 'votings/votings_list.html'
    context_object_name = 'votings'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Voting.objects.filter(start_time__gte = timezone.now())

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Nadchodzące głosowania"
        return context



class VoteDetailView(DetailView):
    model = Voting
    template_name = 'votings/voting_detail.html'
    context_object_name = 'voting'


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        voting = context['voting']
        options = []
        user_vote = None
        if self.request.user.is_authenticated:
            user_vote = Vote.objects.filter(user=user, voting=voting).first()

        if voting.voting_type == 'U':
            options = Vote.VOTE_CHOICES
            if user_vote:
                context['selected_option'] = user_vote.vote_option_for_usual 
        elif voting.voting_type == 'O':
            options = voting.votingoption_set.all()
            if user_vote:
                context['selected_option'] = user_vote.option
        if voting.has_ended():
            context['options'] = voting.get_votes_percentages()
        else:
            context['options'] = options
        return context

    def post(self, request, *args, **kwargs):
        voting = self.get_object()
        if request.user.is_authenticated and voting.is_current():
            option_id = request.POST['option']
            try:
                existed_vote = Vote.objects.filter(voting=voting, user=request.user).first()
                if voting.voting_type == "O":
                    if existed_vote and option_id != existed_vote.option.id:
                        existed_vote.delete()

                    Vote.objects.get_or_create(option_id=option_id, voting=voting, user=request.user)
                else:
                    if existed_vote and option_id != existed_vote.vote_option_for_usual:
                        existed_vote.delete()
                    Vote.objects.get_or_create(vote_option_for_usual=option_id, voting=voting, user=request.user)
            except ValidationError as validation_error:
                return JsonResponse({'status': 'error', 'message': validation_error.messages}, status=400)
            return JsonResponse({'status': 'success'})


class GetOptionsView(View):
    def get(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        options = VotingOption.objects.filter(voting_id=voting_id).values('id', 'option_value')
        return JsonResponse({'options': list(options)})