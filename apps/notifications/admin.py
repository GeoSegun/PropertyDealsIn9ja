from django.contrib import admin
from apps.notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_filter = ('notification_type', 'is_seen',)
    list_display = ('notification_type', 'from_user', 'to_user', 'text_preview')
    list_display_links = ('to_user',)
    readonly_fields = (
        'notification_type',
        'to_user',
        'from_user',
        # 'memorial_tribute',
        # 'memorial_gallery',
        # 'memorial_donation',
        # 'donation_by',
        'wallet_transaction',
        'text_preview',
        'message',
        'is_seen',
    )
    # search_fields = ()


admin.site.register(Notification, NotificationAdmin)
