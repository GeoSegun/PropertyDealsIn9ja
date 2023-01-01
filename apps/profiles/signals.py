import logging

from django.core.files.storage import default_storage
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from propertyDealsIn9ja.settings import AUTH_USER_MODEL
from propertyDealsIn9ja.utils import get_phone_country
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    phone = get_phone_country(f"{instance.phone}")
    if created:
        Profile.objects.create(user=instance, country=phone)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f"{instance}'s profile created")


@receiver(pre_delete, sender=Profile)
def profile_image_delete(sender, instance, **kwargs):
    if instance.image:
        default_storage.delete(instance.image)
