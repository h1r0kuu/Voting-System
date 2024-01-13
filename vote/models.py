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
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 1000, validators=[MinLengthValidator(100)])
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    VOTING_TYPE_CHOICES = [
        ("U","USUAL"),
        ("O","OPTIONAL"),
    ]
    voting_type = models.CharField(choices=VOTING_TYPE_CHOICES, max_length=1, default = VOTING_TYPE_CHOICES[0][0])
    quorum = models.PositiveIntegerField(default = 51, validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_time = models.DateTimeField(null = False, default = timezone.now)
    end_time = models.DateTimeField(null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    options = models.ManyToManyField('VotingOption', related_name = '+')

    def has_image_option(self) -> bool:
        for option in self.options.all():
            if option.image is not None:
                return True
        return False

    def is_current(self):
        now = timezone.now()
        return self.start_time < now and self.end_time > now 

    def is_ended(self):
        return self.end_time < timezone.now()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Voting"
        verbose_name_plural = "Votings"


class VotingOption(models.Model):
    image = models.ImageField(upload_to='uploads/', null=True)
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

    def clean(self):
        if self.voting.is_current == False:
            raise ValidationError("That vote is not taking place now")
        vote = Vote.objects.filter(user = self.user, voting = self.voting).first()
        if vote is not None:
            raise ValidationError("The user has already left a vote in this voting")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Vote, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.voting.title} {self.user.get_full_name()} {self.option.option_value}"

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"