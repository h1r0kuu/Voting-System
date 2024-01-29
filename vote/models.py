from django.db import models
from account_system.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.utils import timezone


class Voting(models.Model):
    VOTING_TYPE_CHOICES = [
        ("U","USUAL"),
        ("O","OPTIONAL"),
    ]

    title = models.CharField(max_length = 100, validators=[MinLengthValidator(15)], verbose_name = "tytuł")
    description = models.CharField(max_length = 1000, validators=[MinLengthValidator(100)], verbose_name = "opis")
    voting_type = models.CharField(choices=VOTING_TYPE_CHOICES, max_length=1, default = VOTING_TYPE_CHOICES[0][0], verbose_name = "typ głosowania")
    quorum = models.PositiveIntegerField(default = 51, validators=[MaxValueValidator(100)], verbose_name = "kworum")
    relative_majority = models.BooleanField(default=True, verbose_name = "większość bezwzględna")
    creator = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, verbose_name = "twórca")
    open_for_voting = models.BooleanField(default=True, verbose_name = "otwarte do głosowania")
    start_time = models.DateTimeField(null = False, default = timezone.now, verbose_name = "czas rozpoczęcia")
    end_time = models.DateTimeField(null = False, verbose_name = "czas zakończenia")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = "utworzony w")

    def clean(self):
        time_difference_minutes = (self.end_time - self.start_time).total_seconds() / 60

        if time_difference_minutes < 60:
            raise ValidationError({"end_time": "Czas zakończenia powinien być dłuższy od czasu rozpoczęcia co najmniej o 1 godzinę."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Voting, self).save(*args, **kwargs)
        if self.id and self.voting_type == "O":
            VotingOption.objects.get_or_create(voting=self, option_value="Wstrzymuje się")

    def is_current(self):
        now = timezone.now()
        return self.start_time < now and self.end_time > now 

    def has_started(self):
        return self.start_time < timezone.now()
    
    def has_ended(self):
        return self.end_time < timezone.now()


    @property
    def current_quorum(self):
        total_users = User.objects.count()
        voted_users = self.vote_set.count()
        return int((voted_users / total_users) * 100)
    
    def get_result(self):
        if self.current_quorum >= self.quorum:
            if self.voting_type == 'O':
                return {"status": True, "winner": self.get_votes_percentages()[0][1]}
            elif self.voting_type == 'U':
                my_dict = {key: value for value, key in self.get_votes_percentages()}
                votes_for = my_dict['Tak']
                votes_against = my_dict['Nie']
                votes_abstain = my_dict['Wstrzymuje się']

                if self.relative_majority:  # Relative majority
                    if votes_for > (votes_against + votes_abstain):
                        return {"status": True, "winner": 'Tak'}
                    else:
                        return {"status": False, "winner": "Głosowanie jest nieważne większość bezwzględna nie spełniona"}
                else: 
                    if votes_for > votes_against:
                        return {"status": True, "winner": 'Tak'}
                    else:
                        return {"status": False, "winner": "Głosowanie jest nieważne większość względna nie spełniona"}
        else:
            return {"status": False, "winner": "Głosowanie jest nieważne kworum nie został spełniony"}

    def get_votes_percentages(self):
        if self.id is not None:
            list_of_votes = self.vote_set.all()
            votes_count = list_of_votes.count()
            if len(list_of_votes) > 0:
                if self.voting_type == 'U':
                    list_of_votes = [
                        (
                            round((list_of_votes.filter(vote_option_for_usual=vote_choice[0]).count() * 100) / votes_count, 1),
                            vote_choice[1]
                        )
                            for vote_choice in Vote.VOTE_CHOICES
                    ]
                elif self.voting_type == 'O':
                    options = self.votingoption_set.all()
                    list_of_votes = [
                        (
                            round((list_of_votes.filter(option=option).count() * 100) / votes_count, 1), 
                            option.option_value
                        )
                        for option in options
                    ]
                list_of_votes.sort(reverse=True, key=lambda x: x[0])
            return list_of_votes

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Głosowanie"
        verbose_name_plural = "Głosowania"
        ordering = ["end_time"]


class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True, verbose_name = "obraz")
    option_value = models.CharField(max_length = 50, verbose_name = "wartość opcji")

    def clean(self):
        if self.voting_id is not None and self.voting.voting_type == 'U':
            raise ValidationError("Nie można utworzyć opcji dla zwykłego głosowania")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(VotingOption, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.option_value}'
    
    class Meta:
        verbose_name = "Opcja głosowania"
        verbose_name_plural = "Opcje głosowania"
        

class Vote(models.Model):
    VOTE_CHOICES = [
        ('Y', 'Tak'),
        ('N', 'Nie'),
        ('A', 'Wstrzymuje się'),
    ]

    user = models.ForeignKey(User, on_delete = models.RESTRICT, verbose_name = "twórca")
    voting = models.ForeignKey(Voting, on_delete = models.RESTRICT, verbose_name = "głosowanie")
    option = models.ForeignKey(VotingOption, on_delete = models.RESTRICT, null = True, blank = True, verbose_name = "opcja")
    vote_option_for_usual = models.CharField(choices=VOTE_CHOICES, max_length=1, null = True, blank = True, verbose_name = "Opcja dla zwykłego głosowania")

    def clean(self):
        if self.voting_id is not None:
            if self.voting.voting_type == 'U':
                if self.option_id is not None:
                    raise ValidationError({"option":"Możesz wybrać tylko Tak, Nie lub Wstrzymaj się. To pole było puste"})
                elif self.vote_option_for_usual is None:
                    raise ValidationError({"vote_option_for_usual":"Należy wybrać opcję zwykłego głosowania"})

            elif self.voting.voting_type == 'O':
                if self.vote_option_for_usual is not None:
                    raise ValidationError({"vote_option_for_usual": "Nie możesz wybrać opcję, które jest przeznaczone do zwykłego głosowania"})
                elif self.option_id is None:
                    raise ValidationError({"option":"Należy wybrać opcję"})

            vote = Vote.objects.filter(user=self.user, voting=self.voting).first()
            if vote is not None:
                raise ValidationError({"vote":"Zostawiłeś już głos w tym głosowaniu"})


    def save(self, *args, **kwargs):
        self.full_clean()
        super(Vote, self).save(*args, **kwargs)


    def __str__(self):
        string = f"{self.voting.title} {self.user.get_full_name()} "
        if self.voting.voting_type == "U":
            string += self.vote_option_for_usual
        else:
            string += self.option.option_value
        return string

    class Meta:
        verbose_name = "Głos"
        verbose_name_plural = "Głosy"