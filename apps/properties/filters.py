import django_filters
from django import forms

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    property_type = django_filters.ChoiceFilter(choices=Property.PropertyTypes.choices, empty_label=('Types'))
    property_status = django_filters.ChoiceFilter(choices=Property.PropertyStatus.choices, empty_label=('Status'))
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Property
        fields = [
            "name",
            "property_type",
            "property_status",
            "uploaded_by__business_name",
            "no_bed_room",
            "no_bath_room",
            "state",
            "city",
        ]


