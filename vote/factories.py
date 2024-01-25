import random
from faker import Faker
import factory.fuzzy
import factory
from factory.django import DjangoModelFactory
from .models import *
from account_system.models import User
import datetime
from datetime import timedelta


fake = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: fake.user_name() + str(n) + fake.user_name()[:2]) 
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("user_name")

class VotingFactory(DjangoModelFactory):
    class Meta:
        model = Voting

    title = factory.Faker(
        "sentence",
        nb_words=8,
        variable_nb_words=True
    )
    description = factory.Faker(
        "paragraph",
        nb_sentences=10
    )
    voting_type = factory.fuzzy.FuzzyChoice(Voting.VOTING_TYPE_CHOICES, getter=lambda c: c[0])
    quorum = factory.Faker("pyint", min_value = 20, max_value = 80)
    relative_majority = factory.Faker("pybool", truth_probability = 50)
    creator = factory.SubFactory(UserFactory)
    open_for_voting = factory.Faker("pybool", truth_probability = 70)
    start_time = factory.Faker("date_time_between", start_date="-1d", end_date="+1d", tzinfo=datetime.timezone.utc)
    end_time = factory.LazyAttribute(lambda o: o.start_time + timedelta(days=random.randint(1, 2)))


class VotingOptionFactory(DjangoModelFactory):
    class Meta:
        model = VotingOption

    voting = factory.SubFactory(VotingFactory)
    image = factory.Maybe(
        factory.LazyFunction(lambda: fake.pybool(20)),
        yes_declaration=factory.django.ImageField(color="blue"),
        no_declaration=None
    ) 

    option_value = factory.Sequence(lambda n: fake.text(10).replace(".", " ") + fake.text(5))


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    voting = factory.SubFactory(VotingFactory)
    option = factory.SubFactory(VotingOptionFactory)
    vote_option_for_usual =  factory.fuzzy.FuzzyChoice(Vote.VOTE_CHOICES, getter=lambda c: c[0])