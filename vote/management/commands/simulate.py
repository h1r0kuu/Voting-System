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
    help = 'Symulacja tworzenia danych dla systemu głosowań'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Usuwanie starych danych...")
        models = [Vote, User, Voting, VotingOption]
        for m in models:
            self.stdout.write(f"Usuwanie starych danych dla modelu {m.__name__}")
            if m is User:
                m.objects.exclude(is_superuser=True).delete()
            else:
                m.objects.all().delete()
        admin_group, _ = Group.objects.get_or_create(name='admin')
        sekretarz_group, _ = Group.objects.get_or_create(name='sekretarz')
        uzytkownik_group, _ = Group.objects.get_or_create(name='użytkownik')

        self.stdout.write("Tworzenie nowych danych...")
        self.stdout.write("Tworzenie nowych danych modelu User")
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

        self.stdout.write("Tworzenie nowych danych modelu Voting")
        votings = []
        for _ in range(NUM_VOTINGS):
            voting = VotingFactory(creator = random.choice(users))
            if voting.voting_type == 'O':
                for _ in range(VOTING_OPTIONS_PER_VOTING):
                    VotingOptionFactory(voting = voting)
            votings.append(voting)

        self.stdout.write("Tworzenie nowych danych modelu Vote")
        for i in range(NUM_VOTINGS):
            voting = votings[i]
            for user in users:
                chance_to_vote = random.random()
                if chance_to_vote > 0.25 and chance_to_vote < 0.85:
                    if voting.is_current() and voting.open_for_voting:
                        option = None
                        if voting.voting_type == 'O':
                            option = VotingOption.objects.filter(voting=voting).order_by('?').first()
                            VoteFactory(user=user, voting=voting, option=option, vote_option_for_usual = None)
                        else:
                            VoteFactory(user=user, voting=voting, option=None)

        self.stdout.write(self.style.SUCCESS('Symulacja danych zakończona.'))
