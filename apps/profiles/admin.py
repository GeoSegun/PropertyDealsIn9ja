from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'slug',
        'gender',
        'country',
        'city'
    ]
    list_filter = ['gender', 'country', 'city']
    list_display_links = ['id', 'slug']
    readonly_fields = (
        'user',
    )


admin.site.register(Profile, ProfileAdmin)
