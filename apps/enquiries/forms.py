from django.forms import ModelForm
from apps.enquiries.models import Enquiry


class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "enquiry_state",
            "enquiry_city",
            "enquiry_property_type",
            "enquiry_property_status",
            "enquiry_description",
            "enquiry_budget_min",
            "enquiry_budget_max",
            "inspection_date",
        ]
