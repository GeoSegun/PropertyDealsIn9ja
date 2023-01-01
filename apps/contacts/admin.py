from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'phone',
        'subject',
        'message',
        'date',
    )
    list_filter = ('date',)
    search_fields = ('name',)
