import datetime

from autoslug import AutoSlugField
from django.core.files.storage import default_storage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from apps.accounts.models import User
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _

from apps.notifications.models import Notification


class AgentQuerySet(models.query.QuerySet):
    def is_an_active_agent(self):
        return self.filter(agent_active=True)


class AgentManager(models.Manager):
    def get_queryset(self):
        return AgentQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().is_an_active_agent()


class Agent(models.Model):
    business_user = models.OneToOneField(User, related_name='agent', on_delete=models.CASCADE, primary_key=True)
    business_name = models.CharField(max_length=150, blank=True, null=True)
    slug = AutoSlugField(populate_from='business_name', unique_with='date_registered', unique=True, always_update=True)
    business_email = models.EmailField(max_length=150, blank=True, null=True)
    business_phone = PhoneNumberField(blank=True, null=True)
    business_logo = models.ImageField(upload_to='agent_photos', blank=True, null=True)
    t_and_c = models.BooleanField(default=True)
    agent_active = models.BooleanField(default=True)
    is_an_agency = models.BooleanField(default=False)
    agency_description = models.TextField(blank=True, null=True)
    my_paid_enquiries = models.ManyToManyField("enquiries.Enquiry", related_name="agent_enquiries", blank=True)
    agency_agents = models.ManyToManyField('accounts.User', related_name="agency_agents", blank=True,)
    state = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    land_mark_area = models.CharField(max_length=150, blank=True, null=True)
    street_address = models.CharField(max_length=150, blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    rating_aggregate = models.CharField(max_length=100, blank=True, null=True, default="0")

    # objects = AgentManager()

    def __str__(self):
        return f"{self.business_name}"

    def get_business_phone(self):
        if self.business_phone:
            return f"{self.business_phone}"
        return f"{self.business_user.phone}"
    
    def get_business_email(self):
        if self.business_email:
            return f"{self.business_email}"
        return f"{self.business_user.email}"
    
    def get_business_address(self):
        return f"{self.street_address} {self.city} {self.state} {self.business_user.profile.country}"

    def get_absolute_url(self):
        return reverse('agents:agent_detail', kwargs={'slug': self.slug})
    
    def business_logo_url(self):
        if self.business_logo:
            return self.business_logo.url
        return "images/header-logo2.png"

    def save(self, *args, **kwargs):
        agent_instance = self.business_user.username
        get_current_user = User.objects.get(username=agent_instance)
        try:
            get_current_user.is_agent = True
            get_current_user.save()
        except ModuleNotFoundError:
            get_current_user.is_agent = False
            get_current_user.save()
            get_current_user.refresh_from_db()
        super(Agent, self).save(args, kwargs)


# === Deactivate user as agent & delete agent address if agent account was deleted ===
@receiver(pre_delete, sender=Agent)
def agent_pre_delete_receiver(sender, instance, *args, **kwargs):
    current_user_agent = User.objects.get(username=instance.business_user.username)
    print(current_user_agent.username)
    current_user_agent.is_an_agent = False
    current_user_agent.save()


class Review(models.Model):
    # class Range(models.IntegerChoices):
    #     RATING_1 = 1, _("Poor")
    #     RATING_2 = 2, _("Fair")
    #     RATING_3 = 3, _("Good")
    #     RATING_4 = 4, _("Very Good")
    #     RATING_5 = 5, _("Excellent")
    user = models.ForeignKey("accounts.User", related_name="user_review", on_delete=models.CASCADE, blank=True, null=True)
    agent = models.ForeignKey("agents.Agent", related_name="agent_review", on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent", default=0)
    comment = models.TextField(blank=True, null=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.agent} rated at {self.rating}"
    
    class Meta:
        # Please only use when creating a unique model...
        unique_together = ["user", "agent"]
        # ordering = ["date_added"]


@receiver(post_save, sender=Review)
def agent_review_comment(sender, instance, *args, **kwargs):
    review = instance
    agent = review.agent.business_user
    sender = review.user
    text_preview = review.comment[:50]
    message = f"{sender} just reviewed your agency."
    notify = Notification(
        agent_message=agent,
        from_user=sender,
        to_user=agent,
        text_preview=text_preview,
        notification_type=5,
        message=message,
    )
    notify.save()


class AgentMessage(models.Model):
    agent = models.ForeignKey(to="Agent", on_delete=models.CASCADE, related_name='agent_msg', blank=True, null=True)
    msg_from = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    msg_content = models.TextField(blank=True, null=True)
    msg_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.msg_content, self.msg_from)

    class Meta:
        ordering = ['msg_on']


@receiver(post_save, sender=AgentMessage)
def agent_recieve_message(sender, instance, *args, **kwargs):
    msg = instance
    agent = msg.agent.business_user
    sender = msg.msg_from
    text_preview = msg.msg_content[:50]
    message = f"You have a new message from {sender}..."
    notify = Notification(
        agent_message=msg,
        from_user=sender,
        to_user=agent,
        text_preview=text_preview,
        notification_type=3,
        message=message,
    )
    notify.save()
