from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from apps.common.models import TimeStampedUUIDModel
from apps.notifications.models import Notification


class InboxMessage(TimeStampedUUIDModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='user')
    msg_sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='from_user')
    msg_receiver = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='to_user')
    message = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.msg_sender} sent a message to {self.msg_receiver}'s inbox"

    def send_message(from_user, to_user, message):
        sender_message = InboxMessage(
            user=from_user,
            msg_sender=from_user,
            msg_receiver=to_user,
            message=message,
            is_seen=True
        )
        sender_message.save()

        recipient_message = InboxMessage(
            user=to_user,
            msg_sender=from_user,
            msg_receiver=from_user,
            message=message,
        )
        recipient_message.save()

    def get_messages(user):
        users = []
        messages = InboxMessage.objects.filter(user=user).values("msg_receiver").annotate(last=Max('created_at')).order_by('-last')
        # print(InboxMessage.objects.filter(user=user))
        for msg in messages:
            print(f"from model level reciever is {msg['msg_receiver']}")
            users.append({
                'user': User.objects.get(pk=msg['msg_receiver']),
                'last': msg['last'],
                'unread': InboxMessage.objects.filter(user=user, msg_receiver__pk=msg['msg_receiver'], is_seen=False).count()
            })
        return users


@receiver(post_save, sender=InboxMessage)
def user_recieve_message(sender, instance, *args, **kwargs):
    msg = instance
    user = msg.msg_receiver
    sender = msg.msg_sender
    text_preview = msg.message[:50]
    message = f"You have a new message from {sender}..."
    notify = Notification(
        inbox_message=msg,
        from_user=sender,
        to_user=user,
        text_preview=text_preview,
        notification_type=3,
        message=message,
    )
    notify.save()
