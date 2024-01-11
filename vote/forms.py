from django import forms
from .models import *


class VotingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Voting
        fields = '__all__'