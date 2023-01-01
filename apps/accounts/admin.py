from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _


class MyAdmin(UserAdmin):
    # The forms to add and change user instances
    ordering = ["email"]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User
    # readonly_fields = (
    #     'balance',
    # )
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_agent', 'is_active',)
    list_display_links = ["username"]
    list_filter = ('email', 'full_name', 'is_staff', 'date_joined',)
    fieldsets = (
        (
            _("Login Credentials"),
            {'fields': ('email', 'password',)}
        ),
        (
            _('Personal info'), {'fields': ('username', 'full_name', 'phone',)}
        ),
        (
            _('Permissions and Groups'),
            {
                'fields': ('is_active', 'is_agent', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
        (
            _("Important Dates"),
            {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'phone', 'password', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email', 'full_name', 'phone',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, MyAdmin)
