from django.contrib.auth.models import Group, Permission


def create_default_groups():
    permissions_list = Permission.objects.all()

    admin_group, _ = Group.objects.get_or_create(name='admin')
    admin_group.permissions.set(permissions_list)

    user_group, _ = Group.objects.get_or_create(name='użytkownik')
    user_group.permissions.set(permissions_list.filter(content_type__app_label='vote', codename__in=[
        'can_vote'    
    ]).all())

    sekretarz_group, _ = Group.objects.get_or_create(name='sekretarz')
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
    sekretarz_group.permissions.add(permissions_list.get(content_type__app_label='dumpdata', codename__in=[
        'add_dumpdata'
    ]))