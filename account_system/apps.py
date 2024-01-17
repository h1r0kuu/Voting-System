from django.apps import AppConfig


class AccountSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_system'
    
    def ready(self):
        import account_system.signals