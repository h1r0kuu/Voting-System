from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    pass


class Voting(models.Model):
    VOTING_TYPE_CHOICES = [
        ("U","USUAL"),
        ("O","OPTIONAL"),
    ]

    title = models.CharField(max_length = 100, validators=[MinLengthValidator(20)])
    description = models.CharField(max_length = 1000, validators=[MinLengthValidator(100)])
    voting_type = models.CharField(choices=VOTING_TYPE_CHOICES, max_length=1, default = VOTING_TYPE_CHOICES[0][0])
    quorum = models.PositiveIntegerField(default = 51, validators=[MinValueValidator(1), MaxValueValidator(100)])
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    open_for_voting = models.BooleanField(default=True)
    start_time = models.DateTimeField(null = False, default = timezone.now)
    end_time = models.DateTimeField(null = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def clean(self):
        time_difference_minutes = (self.end_time - self.start_time).total_seconds() / 60

        if time_difference_minutes < 60:
            raise ValidationError({"end_time": "End time should be greater than start time at least by 1 hour"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Voting, self).save(*args, **kwargs)

    def is_current(self):
        now = timezone.now()
        return self.start_time < now and self.end_time > now 

    def is_ended(self):
        return self.end_time < timezone.now()

    def get_specific_vote(self):
        if self.voting_type == 'U':
            try:
                return self.usualvoting
            except UsualVoting.DoesNotExist:
                return None
        elif self.voting_type == 'O':
            try:
                return self.optionalvoting
            except OptionalVoting.DoesNotExist:
                return None
        else:
            return None

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Voting"
        verbose_name_plural = "Votings"

class UsualVoting(models.Model):
    voting = models.OneToOneField(Voting, on_delete=models.CASCADE, primary_key=True)
    relative_majority = models.BooleanField(verbose_name = "większość bezwzględna", default=True)


    class Meta:
        verbose_name = "Głosowanie zwykłe"
        verbose_name_plural = "Głosowania zwykłe"


class OptionalVoting(models.Model):
    voting = models.OneToOneField(Voting, on_delete=models.CASCADE, primary_key=True)
    voting_options = models.ManyToManyField('VotingOption', related_name = 'options')


    class Meta:
        verbose_name = "Głosowanie na opcje"
        verbose_name_plural = "Głosowania na opcje"


class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    option_value = models.CharField(max_length = 50, unique = True)

    def clean(self):
        if self.voting_id is not None and self.voting.voting_type == 'U':
            raise ValidationError("You cannot create option for usual voting")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(VotingOption, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.option_value}'
    
    class Meta:
        verbose_name = "Voting option"
        verbose_name_plural = "Voting options"
        

class Vote(models.Model):
    VOTE_CHOICES = [
        ('Y', 'Tak'),
        ('N', 'Nie'),
        ('A', 'Wstrzymuje się'),
    ]

    user = models.ForeignKey(User, on_delete = models.RESTRICT)
    voting = models.ForeignKey(Voting, on_delete = models.RESTRICT)
    option = models.ForeignKey(VotingOption, on_delete = models.RESTRICT, null = True, blank = True)
    vote_option_for_usual = models.CharField(choices=VOTE_CHOICES, max_length=1, null = True, blank = True)

    def clean(self):
        if self.voting_id is not None:
            if not self.voting.is_current() or not self.voting.open_for_voting:
                raise ValidationError("That vote is not taking place now")

            if self.voting.voting_type == 'U':
                if self.option_id is not None:
                    raise ValidationError({"option":"You can choose only Yes, No, or Abstain make this field blank"})
                elif self.vote_option_for_usual is None:
                    raise ValidationError({"vote_option_for_usual":"You should choose an option for usual voting"})

            elif self.voting.voting_type == 'O':
                if self.vote_option_for_usual is not None:
                    raise ValidationError({"vote_option_for_usual": "You can't choose options that are for usual voting"})
                elif self.option_id is None:
                    raise ValidationError({"option":"You should choose an option"})

            vote = Vote.objects.filter(user=self.user, voting=self.voting).first()
            if vote is not None:
                raise ValidationError("You already left a vote in this voting")


    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Vote, self).save(*args, **kwargs)

    def __str__(self):
        string = f"{self.voting.title} {self.user.get_full_name()} "
        if self.voting.voting_type == "U":
            string += self.vote_option_for_usual
        else:
            string += self.option.option_value
        return string

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"