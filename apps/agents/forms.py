from django.forms import ModelForm
from apps.agents.models import Agent


class SingleAgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = [
            "business_name",
            "business_email",
            "business_phone",
            "business_logo",
            "state",
            "city",
            "street_address",
        ]


class AgencyForm(ModelForm):
    class Meta:
        model = Agent
        fields = [
            "business_name",
            "business_email",
            "business_phone",
            "agency_description",
            "business_logo",
            "state",
            "city",
            "street_address",
        ]
