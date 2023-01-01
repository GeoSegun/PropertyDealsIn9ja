from django.contrib import admin
# from guardian.admin import GuardedModelAdmin

from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'from_user',
        'to_agent',
        'slug',
        'enquiry_state',
        'enquiry_city',
        'enquiry_Address',
        'enquiry_property_type',
        'enquiry_property_status',
        'enquiry_description',
        'enquiry_budget_min',
        'enquiry_budget_max',
        'enquiry_price',
        'enquiry_on_promo',
        'inspection_date',
        'status',
        'enquiry_date',
    )
    search_fields = ('slug',)