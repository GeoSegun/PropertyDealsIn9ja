from django.db import models
from django.utils import timezone


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Transaction_Message'),
        (2, 'Property_Message'),
        (3, 'Inbox_Message'),
        (4, 'Enquiry_message'),
        (5, 'Review_Message'),
        (6, 'Property_Comment'),
    )
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    to_user = models.ForeignKey('accounts.User', related_name='notification_to', on_delete=models.CASCADE, blank=True, null=True)
    from_user = models.ForeignKey('accounts.User', related_name='notification_from', on_delete=models.CASCADE, blank=True, null=True)
    from_admin = models.CharField(max_length=100, blank=True, null=True, default="System Notification")
    wallet_transaction = models.ForeignKey('wallets.WalletTransaction', related_name='wallet_transaction_notifications', on_delete=models.CASCADE, blank=True, null=True)
    property = models.ForeignKey('properties.Property', related_name='property_notifications', on_delete=models.CASCADE, blank=True, null=True)
    inbox_message = models.ForeignKey('inboxes.InboxMessage', related_name="inbox_msg_notification", on_delete=models.CASCADE, blank=True, null=True)
    review = models.ForeignKey('agents.Review', related_name='review_notifications', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey('properties.Comment', related_name='comment_notifications', on_delete=models.CASCADE, blank=True, null=True)
    text_preview = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=225, blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.notification_type} -> {self.to_user.username}"
