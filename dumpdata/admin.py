from django.contrib import admin    
from .models import Dumpdata
from .utils import create_dumpdate_archive


@admin.register(Dumpdata)
class DumpdataAdmin(admin.ModelAdmin):
    change_form_template = 'admin/dumpdata/add_form.html'
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    def has_view_permission(self, request, obj=None) -> bool:
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return create_dumpdate_archive(obj.archive_password)