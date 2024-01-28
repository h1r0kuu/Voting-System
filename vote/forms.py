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
    
    def clean_voting(self):
        voting = self.cleaned_data['voting']
        if not voting.is_current() or not voting.open_for_voting:
            raise forms.ValidationError("To głosowanie nie odbywa się teraz")

class ArchiveForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)