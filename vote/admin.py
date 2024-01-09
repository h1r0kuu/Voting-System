from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)

@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    pass

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass

@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    pass