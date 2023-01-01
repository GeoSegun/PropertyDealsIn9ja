from autoslug import AutoSlugField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel
from apps.notifications.models import Notification


class EnquiryQuerySet(models.query.QuerySet):
    def is_an_open_enquiry(self):
        return self.filter(is_open=True)


class EnquiryManager(models.Manager):
    def get_queryset(self):
        return EnquiryQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().is_an_open_enquiry()


class Enquiry(TimeStampedUUIDModel):
    class Types(models.TextChoices):
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

    class Status(models.TextChoices):
        FOR_RENT = 'For Rent'
        FOR_SALE = 'For Sale'
        AUCTION = 'Auction'
        SOLD = 'Sold'
        RENTED = 'Rented'

    class EnquiryStatus(models.TextChoices):
        ASSIGNED = 'Assigned'
        OPEN = 'Open'

    from_user = models.ForeignKey("accounts.User", related_name="user_enquiries", on_delete=models.DO_NOTHING, blank=True, null=True)
    to_agent = models.ForeignKey("agents.Agent", related_name="agent_enquiries", on_delete=models.DO_NOTHING, blank=True, null=True)
    enquiry_state = models.CharField(help_text="State", max_length=144, blank=True, null=True)
    enquiry_city = models.CharField(help_text="City/LGA", max_length=144, blank=True, null=True)
    enquiry_Address = models.CharField(help_text="Local Area/Bustops/Park", max_length=144, blank=True, null=True)
    slug = AutoSlugField(populate_from='from_user', unique_with='enquiry_date', unique=True, always_update=True)
    enquiry_property_type = models.CharField(choices=Types.choices, max_length=144, blank=True, null=True, default="Type")
    enquiry_property_status = models.CharField(choices=Status.choices, max_length=144, blank=True, null=True, default="Status")
    enquiry_description = models.TextField(help_text="Tell us more about what you need.", blank=True, null=True)
    enquiry_budget_min = models.DecimalField(help_text="Your Minimum Budget", max_digits=10, decimal_places=2)
    enquiry_budget_max = models.DecimalField(help_text="Your Maximum Budget", max_digits=10, decimal_places=2)
    enquiry_price = models.DecimalField(help_text="0.00", max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    enquiry_on_promo = models.BooleanField(default=True)
    inspection_date = models.DateTimeField()
    # is_open = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=EnquiryStatus.choices, blank=True, null=True, default="Open")
    enquiry_date = models.DateTimeField(default=timezone.now)
    # objects = EnquiryManager()

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ("-enquiry_date",)

    def __str__(self):
        return f"{self.enquiry_property_type}-{self.enquiry_property_status}"

    # def get_absolute_url(self):
    #     return redirect('enquiries:my_enquiry_list')

    @property
    def name(self):
        return f"{self.enquiry_property_type} Enquiry for {self.enquiry_property_status}"

    @property
    def enquiry_address(self):
        return f"{self.enquiry_state}, {self.enquiry_city}"


@receiver(post_save, sender=Enquiry)
def user_add_enquiry_notification(sender, instance, *args, **kwargs):
    enquiry = instance
    sender = enquiry.from_user
    message = f"Your enquiry was added successfully an Agent will get back to you shortly."
    notify = Notification(
        from_user=sender,
        to_user=sender,
        notification_type=4,
        message=message,
    )
    notify.save()
