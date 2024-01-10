from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    pass


class Voting(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    VOTING_TYPE_CHOICES = [
        ("U","USUAL"),
        ("O","OPTIONAL"),
    ]
    voting_type = models.CharField(choices=VOTING_TYPE_CHOICES, max_length=1, default = VOTING_TYPE_CHOICES[0][0])
    kworum = models.PositiveIntegerField(default = 51, validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_time = models.DateTimeField(null = False, default = timezone.now())
    end_time = models.DateTimeField(null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    options = models.ManyToManyField('VotingOption', related_name = '+')

    def save(self, *args, **kwargs):
        if not self.id:
            super(Voting, self).save(*args, **kwargs)
        if len(self.options.values()) > 5:
            raise ValidationError("Maximum quantity of options for Voting is 5")
        super(Voting, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Voting"
        verbose_name_plural = "Votings"


class VotingOption(models.Model):
    option_value = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return f'{self.option_value}'
    
    class Meta:
        verbose_name = "Voting option"
        verbose_name_plural = "Voting options"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete = models.RESTRICT)
    voting = models.ForeignKey(Voting, on_delete = models.RESTRICT)
    option = models.ForeignKey(VotingOption, on_delete = models.RESTRICT)

    def __str__(self):
        return f"{self.voting.title} {self.user.get_full_name()} {self.option.option_value}"

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"