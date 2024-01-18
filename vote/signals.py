from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from vote.models import Vote


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'vote':
        ct = ContentType.objects.get_for_model(Vote)
        Permission.objects.get_or_create(codename='can_vote', name='Can Vote', content_type=ct)