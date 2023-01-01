from django import forms
from apps.inboxes.models import InboxMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ('message',)
