from django.contrib import admin


class QuorumFilter(admin.SimpleListFilter):
    title = 'kworum'
    parameter_name = 'quorum'

    def lookups(self, request, model_admin):
        return (
            ("0-25", '0-25 %'),
            ("25-50", '25-50 %'),
            ("50-75", '50-75 %'),
            ("75-100", '75-100 %'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-25':
            return queryset.filter(quorum__lte=25)
        if self.value() == '25-50':
            return queryset.filter(quorum__range=(25, 50))
        if self.value() == '50-75':
            return queryset.filter(quorum__range=(50, 75))
        if self.value() == '75-100':
            return queryset.filter(quorum__gte=75)