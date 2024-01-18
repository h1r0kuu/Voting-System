from django.core.management.base import no_translations
from django.core.management.commands.migrate import Command as MigrateCommand

from account_system.utils import create_default_groups


class Command(MigrateCommand):
    @no_translations
    def handle(self, *args, **options):
        super().handle(*args, **options)
        create_default_groups()