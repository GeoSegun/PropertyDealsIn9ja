from django.db import models


class ChatModel(models.Model):
    msg_sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='sender', default=None)
    # msg_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', default=None)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(max_length=100, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.msg_sender} -> {self.message[:10]}"

    @property
    def get_user_msg_count(self):
        return self.objects.filter(msg_sender=self).filter(is_seen=False).count()

    @property
    def get_user_last_message(self):
        return self.objects.filter(msg_sender=self).order_by('-timestamp').first()


# @receiver(post_save, sender=ChatModel)
# def user_recieve_message(sender, instance, *args, **kwargs):
#     msg = instance
#     # user = msg.user
#     sender = msg.msg_sender
#     text_preview = msg.message[:50]
#     message = f"You have a new message from {sender}..."
#     notify = Notification(
#         user_message=msg,
#         from_user=sender,
#         # to_user=user,
#         text_preview=text_preview,
#         notification_type=4,
#         message=message,
#     )
#     notify.save()
