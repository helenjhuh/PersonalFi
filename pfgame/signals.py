from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import GameProfile


@receiver(post_save, sender=get_user_model(), dispatch_uid="create_GameProfile")
def create_GameProfile(sender, **kwargs):
    instance = kwargs["instance"]
    obj, created = GameProfile.objects.get_or_create(user=instance)
