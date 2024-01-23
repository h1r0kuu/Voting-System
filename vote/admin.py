import zipfile
from django.contrib import admin
from django.urls import reverse
from .forms import *
from .models import *
from django.http import FileResponse
from .utils import RaportPDF
from rangefilter.filters import DateTimeRangeFilterBuilder
from django.utils.html import format_html, html_safe
from .filters import QuorumFilter
import pyzipper


class VotingOptionInline(admin.TabularInline):
    model = VotingOption
    extra = 5
    max_num = 5
    template = 'admin/voting/inline.html'


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'truncated_description', 'creator', 'voting_type', 'quorum', 'current_quorum', 'relative_majority', 'start_time', 'end_time')
    search_fields = ('title', 'description', 'creator__username', 'voting_type', 'quorum', 'start_time', 'end_time')
    actions = ['generate_raport']
    list_filter = ('voting_type',
                   ('start_time', DateTimeRangeFilterBuilder(title="Start time")),
                   ('end_time', DateTimeRangeFilterBuilder(title="End time")),
                   'relative_majority',
                   QuorumFilter
                   )

    form = VotingForm
    inlines = [VotingOptionInline]
    list_per_page = 10
    change_form_template = 'admin/voting/change_form.html'


    def truncated_description(self, obj):
        return format_html(f'<div title="{obj.description}">{obj.description[:50]}...</div>')
    truncated_description.short_description = 'Opis'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'creator':
            kwargs['initial'] = request.user
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.action(description="Wygeneruj raport")
    def generate_raport(self, request, queryset):
        if len(queryset) > 1:
            archive_name = "reports.zip"
            with pyzipper.AESZipFile(archive_name, 'w') as zip_file:
                for obj in queryset:
                    raport = RaportPDF(obj).generate_pdf()
                    zip_file.writestr(f'report_{obj.title}.pdf', raport.getvalue())
            zip_file.close()

            return FileResponse(open(archive_name, 'rb'), as_attachment=True, filename=archive_name)
        
        return RaportPDF(queryset.first()).generate_pdf()

@html_safe
class JSPath:
    def __str__(self):
        return '<script type="text/javascript" rel="stylesheet"> const optionsUrl=\''+reverse("get_voting_options")+'\'</script>'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'voting', 'option', 'vote_option_for_usual')
    search_fields = ('user__username', 'voting__title', 'option__option_value', 'vote_option_for_usual')
    list_per_page = 20

    form = VoteForm
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = (JSPath(), 'js/vote_admin.js',)

@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ('option_value', 'image_tag')
    search_fields = ('option_value',)
    list_per_page = 20


    def image_tag(self, obj):
        html = '<img src="{img}" width="150" height="150">'
        if obj.image:
            return format_html(html, img=obj.image.url)
    image_tag.short_description = 'Obraz'
