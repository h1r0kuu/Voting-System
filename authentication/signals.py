from django.db.models.signals import post_save
from django.dispatch import receiver
from vote.models import User


@receiver(post_save, sender=User)
def set_is_staff(sender, instance, **kwargs):
    if instance.groups.filter(name='sekretarz').exists():
        instance.is_staff = True
        instance.save()