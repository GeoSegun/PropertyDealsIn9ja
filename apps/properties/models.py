from datetime import date
from django.utils import timezone
from autoslug import AutoSlugField
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse

from apps.accounts.models import User
from apps.notifications.models import Notification


def upload_dir(instance, filename):
    return "{}/{}/{}/{}".format("property_uploads", instance.uploaded_by.business_name, instance.name, filename)


def property_media_upload_dir(instance, filename):
    return "{}/{}/{}".format("property_media_uploads", instance.img_property.uploaded_by.business_name, filename)


class Property(models.Model):

    class PropertyTypes(models.TextChoices):
        APARTMENT = 'Apartment'
        LAND = 'Land'
        BQ = 'BQ'
        TERRACE = 'Terrace'
        SEMI_DETACHED = 'Semi Detached'
        FULLY_DETACHED = 'Fully Detached'
        OFFICE = 'Office'
        WAREHOUSE = 'Warehouse'
        COMMERCIAL = 'Commercial'
        OTHER = 'Other'

    class PropertyStatus(models.TextChoices):
        FOR_RENT = 'For Rent'
        FOR_SALE = 'For Sale'
        AUCTION = 'Auction'
        SOLD = 'Sold'
        RENTED = 'Rented'

    class PaymentPlan(models.TextChoices):
        MONTHLY = 'Mthly'
        QUARTERLY = 'Qtly'
        HALF_YEARLY = '1/2Yr'
        ANNUALLY = 'Yr'
        NONE = "None"

    name = models.CharField(max_length=120, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique_with='uploaded_at', unique=True, always_update=True)
    description = models.TextField(help_text="Tell us more about this property...", blank=True, null=True)
    property_image = models.ImageField(help_text="Main View", upload_to=upload_dir, blank=True, null=True)
    exterior_image1 = models.ImageField(help_text="Exterior View1", upload_to=upload_dir, blank=True, null=True)
    exterior_image2 = models.ImageField(help_text="Exterior View2", upload_to=upload_dir, blank=True, null=True)
    interior_image1 = models.ImageField(help_text="Interior View1", upload_to=upload_dir, blank=True, null=True)
    interior_image2 = models.ImageField(help_text="Interior View2", upload_to=upload_dir, blank=True, null=True)
    price = models.DecimalField(help_text="0.00", max_digits=10, decimal_places=2, default=0.00)
    payment_plan = models.CharField(choices=PaymentPlan.choices, max_length=144, blank=True, null=True, default="None")
    tax = models.DecimalField(help_text="Property Tax '10% property tax charged'", max_digits=6, decimal_places=2, default=0.15, blank=True, null=True)
    featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    # property_document = models.FileField(upload_to='user_photos')
    # on_promo = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name="like", default=None, blank=True)
    like_count = models.BigIntegerField(default=0)
    property_type = models.CharField(choices=PropertyTypes.choices, max_length=144, blank=True, null=True, default="Property Type")
    property_status = models.CharField(choices=PropertyStatus.choices, max_length=144, blank=True, null=True, default="Property Status")
    uploaded_by = models.ForeignKey(to="agents.Agent", related_name="properties", on_delete=models.CASCADE, blank=True, null=True)
    plot_area = models.IntegerField(help_text="The plot/size measured in Sqft...", blank=True, null=True)
    no_bed_room = models.IntegerField(blank=True, null=True, help_text="Number of bedroom exception of land", default=0)
    no_bath_room = models.IntegerField(blank=True, null=True, help_text="Number of bathroom  exception of land", default=0)
    state = models.CharField(help_text="State", max_length=144, blank=True, null=True)
    city = models.CharField(help_text="City/LGA", max_length=144, blank=True, null=True)
    local_area = models.CharField(help_text="Nearest Bustop/Local Area", max_length=144, blank=True, null=True)
    street_address = models.CharField(help_text="Street Address/House Number", max_length=144, blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ("-uploaded_at",)
        unique_together = ['name', 'slug']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})

    def check_image_url(self):
        if self.property_image:
            return self.property_image.url
        else:
            return "https://zebejakque-app.s3.us-east-2.amazonaws.com/img/property/1.png"

    @property
    def property_address(self):
        return f"{self.street_address} {self.local_area} {self.city} {self.state} {self.uploaded_by.business_user.profile.country.name}"

    # @property
    # def get_property_images(self):
    #     return self.propertymedia_set.all()


@receiver(post_save, sender=Property)
def user_add_property_notification(sender, instance, *args, **kwargs):
    prop = instance
    sender = "System Notification"
    message = f"Your property of {prop.name} has been approved."
    notify = Notification(
        property=prop,
        from_admin=sender,
        to_user=prop.uploaded_by.business_user,
        notification_type=2,
        message=message,
    )
    notify.save()


# @receiver(post_delete, sender=Property)
# def property_images_delete(sender, instance, **kwargs):
#     if instance.prop_image:
#         default_storage.delete(instance.prop_image)
#     if instance.exterior_image1:
#         default_storage.delete(instance.exterior_image1)
#     if instance.exterior_image2:
#         default_storage.delete(instance.exterior_image2)
#     if instance.interior_image1:
#         default_storage.delete(instance.interior_image1)
#     if instance.interior_image2:
#         default_storage.delete(instance.interior_image2)


class PropertyMedia(models.Model):
    img_property = models.ForeignKey(Property, related_name="property_images", on_delete=models.CASCADE, blank=True, null=True)
    property_image = models.ImageField(help_text="Upload images", upload_to=property_media_upload_dir, blank=True, null=True)
    uploaded_by = models.ForeignKey(User, related_name="my_property_images", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.property_image.url}"


class Comment(models.Model):
    property = models.ForeignKey(
        to="Property",
        on_delete=models.CASCADE,
        related_name='property_comment',
        blank=True,
        null=True
    )
    by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.content, self.by)

    class Meta:
        ordering = ['created_on']


@receiver(post_save, sender=Comment)
def user_add_comment_property(sender, instance, *args, **kwargs):
    comment = instance
    comm_prop = comment.property
    sender = comment.by
    text_preview = comment.content[:50]
    message = f"{comment.by} just commented at {comm_prop.name}"
    notify = Notification(
        comment=comment,
        from_user=sender,
        to_user=comm_prop.uploaded_by.business_user,
        text_preview=text_preview,
        notification_type=6,
        message=message,
    )
    notify.save()
