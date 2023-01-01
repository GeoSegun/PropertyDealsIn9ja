# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Agent, Review


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = (
        'business_user',
        'business_name',
        'slug',
        'business_email',
        'business_phone',
        'business_logo',
        't_and_c',
        'agent_active',
        'state',
        'city',
        'land_mark_area',
        'street_address',
        'date_registered',
    )
    list_filter = (
        'business_user',
        't_and_c',
        'agent_active',
        'date_registered',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        # 'id',
        'user',
        'agent',
        'rating',
        'comment',
    )
    list_filter = ('user', 'agent')
