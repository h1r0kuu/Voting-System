from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Vote

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'vote':
        ct = ContentType.objects.get_for_model(Vote)
        can_vote_permission, permission_created = Permission.objects.get_or_create(codename='can_vote', name='Can Vote', content_type=ct)
        permissions_list = Permission.objects.all()

        admin_group, admin_created = Group.objects.get_or_create(name='admin')
        admin_group.permissions.set(permissions_list)

        user_group, user_created = Group.objects.get_or_create(name='użytkownik')
        user_group.permissions.set([can_vote_permission])

        sekretarz_group, sekretarz_created = Group.objects.get_or_create(name='sekretarz')
        sekretarz_group.permissions.set(permissions_list.filter(content_type__app_label='vote', codename__in=[
            'add_voting',
            'change_voting',
            'delete_voting',
            'view_voting',

            'add_votingoption',
            'change_votingoption',
            'delete_votingoption',
            'view_votingoption',
        ]).all())
