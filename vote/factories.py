import random
from faker import Faker
import factory.fuzzy
import factory
from factory.django import DjangoModelFactory
from .models import *
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
    creator = factory.SubFactory(UserFactory)
    open_for_voting = factory.Faker("pybool", truth_probability = 70)
    start_time = factory.Faker("date_time_between", start_date="-1d", end_date="+1d", tzinfo=datetime.timezone.utc)
    end_time = factory.LazyAttribute(lambda o: o.start_time + timedelta(days=random.randint(1, 2)))


class UsualVotingFactory(DjangoModelFactory):
    class Meta:
        model = UsualVoting

    voting = factory.SubFactory(VotingFactory)
    relative_majority = factory.Faker("pybool")


class VotingOptionFactory(DjangoModelFactory):
    class Meta:
        model = VotingOption

    voting = factory.SubFactory(VotingFactory)
    image = factory.Faker("image_url")
    option_value = factory.Sequence(lambda n: fake.text(5).replace(".", " ") + fake.text(5))


class OptionalVotingFactory(DjangoModelFactory):
    class Meta:
        model = OptionalVoting

    voting = factory.SubFactory(VotingFactory)
    
    @factory.post_generation
    def voting_options(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for option in extracted:
                self.voting_options.add(option)


class VoteFactory(DjangoModelFactory):
    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    voting = factory.SubFactory(VotingFactory)
    option = factory.SubFactory(VotingOptionFactory)
    vote_option_for_usual =  factory.fuzzy.FuzzyChoice(Vote.VOTE_CHOICES, getter=lambda c: c[0])