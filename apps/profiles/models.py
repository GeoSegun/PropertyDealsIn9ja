from autoslug import AutoSlugField
# from cloudinary.models import CloudinaryField
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


def upload_dir(instance, filename):
    return "{}/{}/{}".format("user_photos", instance.user.username, filename)


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='user', unique=True, always_update=True)
    gender = models.CharField(verbose_name=_("Gender"), max_length=20, choices=Gender.choices, default=Gender.OTHER)
    bio = models.TextField(verbose_name=_("About me"), default="Say something about yourself")
    image = models.ImageField(upload_to=upload_dir, blank=True, null=True)
    conversations = models.ManyToManyField('accounts.User', related_name='conversations', blank=True)
    country = CountryField(verbose_name=_("Country"), default="NG", blank=True, null=True)
    state = models.CharField(verbose_name=_("State"), max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=100, blank=True, null=True)
    address = models.CharField(verbose_name=_("Address"), max_length=100, default="", blank=True, null=True)
    favorite_properties = models.ManyToManyField("properties.Property", blank=True)
    birth_day = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'slug': self.slug})
    
    def get_user_address(self):
        return f"{self.address} {self.city} {self.state} {self.country.name}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return 'https://res.cloudinary.com/geetechlab-com/image/upload/v1583147406/nwaben.com/user_azjdde_sd2oje.jpg'

