from django import forms
from .models import *


class VotingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Voting
        fields = '__all__'

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'