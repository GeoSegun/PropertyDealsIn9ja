from django import forms
from django.forms import ModelForm
from apps.properties.models import Property, PropertyMedia


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = [
            "name",
            "description",
            "property_type",
            "property_status",
            "payment_plan",
            "price",
            "plot_area",
            "no_bed_room",
            "no_bath_room",
            "property_image",
            "exterior_image1",
            "exterior_image2",
            "interior_image1",
            "interior_image2",
            "state",
            "city",
            "local_area",
            "street_address",
            "featured",
        ]


class PropertyMediaForm(ModelForm):
    # property_image = forms.ImageField(
    #     label="Image",
    #     # widget=forms.ClearableFileInput(attrs={"multiple": True}),
    # )

    class Meta:
        model = PropertyMedia
        fields = ("property_image",)

