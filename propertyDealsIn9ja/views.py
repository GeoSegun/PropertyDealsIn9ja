from django.db.models import Q
from django.shortcuts import render
from django.views import View

from apps.agents.models import Agent
from apps.properties.filters import PropertyFilter
from apps.properties.models import Property


class HomeView(View):
    template_name = "index.html"

    def get(self, request):
        # latest_for_sale = None
        # latest_for_rent = None
        warehouses = Property.objects.filter(property_type="Warehouse")
        apartments = Property.objects.filter(property_type="Apartment")
        lands = Property.objects.filter(property_type="Land")
        offices = Property.objects.filter(property_type="Office")
        featured_properties = Property.objects.filter(featured=True)[:6]
        agents = Agent.objects.all()[:6]
        location_featured_properties = []
        if self.request.user.is_authenticated:
            location_featured_properties = Property.objects.filter(state=self.request.user.profile.state).filter(featured=True)[:3]
        location_featured_properties = Property.objects.filter(featured=True)[:3]

        property_filter = PropertyFilter(request.GET, queryset=Property.objects.filter(property_status="For Rent"))
        context = {
            "warehouses": warehouses,
            "apartments": apartments,
            "lands": lands,
            "offices": offices,
            "featured_properties": featured_properties,
            "location_featured_properties": location_featured_properties,
            "form": property_filter.form,
            "agents": agents,
        }
        return render(request, self.template_name, context)


def filter_property(request):
    qs = Property.objects.all()
    property_type_exact_query = request.GET.get("property_type_exact_query")
    property_search_contain_query = request.GET.get("property_search_contain_query")

    if property_type_exact_query != '' and property_type_exact_query is not None:
        qs = qs.filter(property_type__iexact=property_type_exact_query)

    if property_search_contain_query != '' and property_search_contain_query is not None:
        qs = qs.filter(Q(name__icontains=property_search_contain_query)
                       | Q(uploaded_by__business_name__icontains=property_search_contain_query)).distinct()
    context = {
        'properties': qs
    }
    return render(request, "filtered_result.html", context)
