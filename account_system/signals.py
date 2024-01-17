from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def set_is_staff(sender, instance, **kwargs):
    if instance.groups.filter(name='admin').exists() or instance.groups.filter(name='sekretarz').exists():
        User.objects.filter(id=instance.id).update(is_staff=True)