from datetime import datetime
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.email
