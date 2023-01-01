import logging
import uuid
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from propertyDealsIn9ja.settings import AUTH_USER_MODEL
from apps.common.models import TimeStampedUUIDModel
from apps.notifications.models import Notification
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)

CURRENCY = (
    ("NGN", "NGN"),
    ("USD", "USD"),
)

STATUS = (
    ("successful", "successful"),
    ("pending", "pending"),
    ("failed", "failed"),
)


class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, related_name="wallet")
    currency = models.CharField(_("currency"), max_length=200, blank=True, null=True, default="NGN")
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, related_name="currency")
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID {self.uid} owner-{self.user.username}"


@receiver(post_save, sender=Profile)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        currency = "NGN" if instance.country == "NG" else "USD"
        Wallet.objects.create(user=instance.user, currency=currency)


@receiver(post_save, sender=Profile)
def save_user_wallet(sender, instance, **kwargs):
    instance.user.wallet.save()
    logger.info(f"{instance}'s wallet created")


class WalletTransaction(TimeStampedUUIDModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, related_name="wallet_transactions")
    transaction_id = models.CharField(_("transaction"), max_length=100)
    currency = models.CharField(_("currency"), max_length=100, choices=CURRENCY, default="NGN", blank=True, null=True)
    amount = models.DecimalField(_("amount"), max_digits=100, decimal_places=2)
    payment_status = models.CharField(_("payment status"), max_length=100, choices=STATUS)
    payment_gateway = models.CharField(_("payment gateway"), max_length=100, default="flutterwave")
    is_in_flow = models.BooleanField(_("concurrences"), default=False)
    transaction_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transactions for {self.wallet} id: {self.transaction_id}"


@receiver(post_save, sender=WalletTransaction)
def user_add_transactions_notification(sender, instance, *args, **kwargs):
    transaction = instance
    sender = transaction.wallet.user
    message = f"Transaction for {transaction.transaction_id} with amount {transaction.currency}{transaction.amount} was initiated.\n Time-stamp: {transaction.created_at}.\n Transaction status: {transaction.payment_status}"
    notify = Notification(
        wallet_transaction=transaction,
        from_user=sender,
        to_user=transaction.wallet.user,
        notification_type=1,
        message=message,
    )
    notify.save()

