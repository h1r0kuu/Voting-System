from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *

admin.site.register(User, UserAdmin)

class VotingOptionInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        if index == 0 and not form.initial.get('votingoption'):
            default_option = VotingOption.objects.filter(option_value='Wstrzymuje sie').first()
            form.fields['votingoption'].initial = default_option
            form.fields['votingoption'].disabled = True
            

class VotingOptionInline(admin.TabularInline):
    model = Voting.options.through
    formset = VotingOptionInlineFormSet
    extra = 5
    min_num = 3
    max_num = 6


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'truncated_description', 'creator', 'voting_type', 'quorum', 'current_quorum', 'start_time', 'end_time')
    search_fields = ('title', 'description', 'creator', 'voting_type', 'quorum', 'start_time', 'end_time')
    exclude = ('options', )

    list_per_page = 10
    form = VotingForm
    inlines = [VotingOptionInline]

    def current_quorum(self, obj):
        total_users = User.objects.count()
        voted_users = obj.vote_set.count()
        return '{}%'.format(int((voted_users / total_users) * 100))

    def truncated_description(self, obj):
        return format_html(f'<div title="{obj.description}">{obj.description[:50]}...</div>')
    truncated_description.short_description = 'Description'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'voting', 'option')
    search_fields = ('user', 'voting', 'option')
    list_per_page = 10


@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ('option_value', 'image')
    search_fields = ('option_value',)
    list_per_page = 10

    def image(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.image.url))
    image.short_description = 'Image'