from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def set_is_staff(sender, instance, **kwargs):
    if instance.groups.filter(name='admin').exists() or instance.groups.filter(name='sekretarz').exists():
        User.objects.filter(id=instance.id).update(is_staff=True)


@receiver(m2m_changed, sender=User.groups.through)
def update_staff_status(sender, instance, action, *args, **kwargs):
    if action == "post_add" or action == "post_remove":
        if instance.groups.filter(name='admin').exists() or instance.groups.filter(name='sekretarz').exists():
            instance.is_staff = True
        else:
            instance.is_staff = False
        instance.save()