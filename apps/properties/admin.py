# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Property, Comment, PropertyMedia


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'featured',
        'property_type',
        'property_status',
        'uploaded_by',
        'plot_area',
        'no_bed_room',
        'no_bath_room',
        'state',
        'city',
        'uploaded_at',
    )
    list_filter = ('payment_plan', 'featured', 'uploaded_by', 'uploaded_at', 'property_status', 'property_type')
    search_fields = ('name', 'slug')
    # prepopulated_fields = {'slug': ['name']}


@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_property', 'property_image')
    list_filter = ('img_property',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'by', 'content', 'created_on')
    list_filter = ('property', 'by', 'created_on')