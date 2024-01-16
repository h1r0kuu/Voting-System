import random

from django.contrib.auth.models import Group
from django.db import transaction
from django.core.management.base import BaseCommand
from vote.models import *
from vote.factories import *


NUM_USERS = 100
NUM_VOTINGS = 50
NUM_USUAL_VOTINGS = NUM_VOTINGS / 2
VOTING_OPTIONS_PER_VOTING = 5

NUM_VOTES = int((NUM_USERS * NUM_VOTINGS) * 0.8)

class Command(BaseCommand):
    help = 'Simulate data creation for the voting system'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Vote, User, Voting, UsualVoting, OptionalVoting, VotingOption]
        for m in models:
            self.stdout.write(f"Deleting old data for {m.__name__}")
            m.objects.all().delete()

        admin_group, _ = Group.objects.get_or_create(name='admin')
        sekretarz_group, _ = Group.objects.get_or_create(name='sekretarz')
        uzytkownik_group, _ = Group.objects.get_or_create(name='użytkownik')

        self.stdout.write("Creating new data...")
        self.stdout.write("Creating new Users")
        users = []
        for _ in range(NUM_USERS):
            user = UserFactory()
            rand_num = random.random()
            if rand_num <= 0.1:
                user.groups.add(admin_group)
            elif rand_num <= 0.25:
                user.groups.add(sekretarz_group)
            else:
                user.groups.add(uzytkownik_group)
            user.save()
            users.append(user)
            print(f'Created user with ID {user.id}')

        self.stdout.write("Creating new Votings")
        votings = []
        for _ in range(NUM_VOTINGS):
            voting = VotingFactory(creator = random.choice(users))
            if voting.voting_type == 'U':
                UsualVotingFactory(voting=voting)
            elif voting.voting_type == 'O':
                options = []
                for _ in range(VOTING_OPTIONS_PER_VOTING):
                    voting_option = VotingOptionFactory(voting = voting)
                    options.append(voting_option)
                optional_voting = OptionalVotingFactory(voting=voting, voting_options=options)
                optional_voting.voting_options.set(options)
            votings.append(voting)

        self.stdout.write("Creating user votes")
        for i in range(NUM_VOTINGS):
            voting = votings[i]
            for user in users:
                chance_to_vote = random.random()
                if chance_to_vote > 0.25 and chance_to_vote < 0.85:
                    if voting.is_current():
                        option = None
                        if voting.voting_type == 'O':
                            option = VotingOption.objects.filter(voting=voting).order_by('?').first()
                            VoteFactory(user=user, voting=voting, option=option, vote_option_for_usual = None)
                        else:
                            VoteFactory(user=user, voting=voting, option=None)

        self.stdout.write(self.style.SUCCESS('Data simulation completed.'))
