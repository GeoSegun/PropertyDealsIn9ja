from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.enquiries.forms import EnquiryForm
from apps.enquiries.models import Enquiry
from apps.wallets.models import Wallet, WalletTransaction
from propertyDealsIn9ja.utils import get_states_only, get_cities_only


class EnquiryListView(ListView):
    model = Enquiry
    paginate_by = 6
    template_name = "enquiries/list.html"
    context_object_name = "enquiries"
    queryset = Enquiry.objects.filter(status="Open")


class EnquiryDetailView(DetailView):
    model = Enquiry
    template_name = "enquiries/detail.html"
    context_object_name = "enquiry"


class EnquiryPaymentView(View):

    def get(self, request, slug):
        enquiry = get_object_or_404(Enquiry, slug=slug)
        wallet = self.request.user.wallet
        if enquiry.enquiry_on_promo:
            # Update the enquiry
            enquiry.to_agent = self.request.user.agent
            enquiry.status = "Assigned"
            enquiry.save(update_fields=['to_agent', 'status'])
            messages.success(request, "Enquiry added to your list")
            return redirect("enquiries:detail", enquiry.slug)
        elif wallet.balance >= enquiry.enquiry_price:
            wallet.balance = F('balance') - enquiry.enquiry_price
            wallet.save()
            # Update the enquiry
            enquiry.to_agent = self.request.user.agent
            enquiry.status = "Assigned"
            enquiry.save(update_fields=['to_agent', 'status'])
            wallet_transaction = WalletTransaction.objects.create(
                wallet=wallet,
                transaction_id=enquiry.name[:6],
                currency=wallet.currency,
                amount=enquiry.enquiry_price,
                payment_status="Success",
            )
            wallet.wallet_transactions.add(wallet_transaction)
            messages.success(request, "Enquiry bought and added to your list")
            return redirect("enquiries:detail", enquiry.slug)
        messages.error(request, "Low balance please fund your wallet")
        return redirect("wallets:fund_wallet", self.request.user.wallet.uid)


class EnquiryCreateView(LoginRequiredMixin, CreateView):
    template_name = "enquiries/create_form.html"
    form_class = EnquiryForm

    def get_context_data(self, **kwargs):
        context = super(EnquiryCreateView, self).get_context_data()
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        context["states"] = get_states_only(file_path)
        return context

    def form_valid(self, form):
        user = self.request.user
        # create address
        state = self.request.POST.get("state")
        city = self.request.POST.get("city")
        enquiry_property_type = form.cleaned_data['enquiry_property_type']
        enquiry_property_status = form.cleaned_data['enquiry_property_status']
        enquiry_description = form.cleaned_data['enquiry_description']
        enquiry_budget_min = form.cleaned_data['enquiry_budget_min']
        enquiry_budget_max = form.cleaned_data['enquiry_budget_max']
        inspection_date = form.cleaned_data['inspection_date']
        print("About to create Enquiry.")
        Enquiry.objects.create(
            from_user=user,
            enquiry_state=state,
            enquiry_city=city,
            enquiry_property_type=enquiry_property_type,
            enquiry_property_status=enquiry_property_status,
            enquiry_description=enquiry_description,
            enquiry_budget_min=enquiry_budget_min,
            enquiry_budget_max=enquiry_budget_max,
            inspection_date=inspection_date,
        ).save()
        print("Enquiry Added.")
        messages.success(self.request, "Enquiry added successfully.")
        if self.request.POST.get('next') != '':
            return redirect(self.request.POST.get('next'))
        return redirect('home')
        # return super(EnquiryCreateView, self).form_valid()


class EnquiryUpdateView(LoginRequiredMixin, UpdateView):
    model = Enquiry
    template_name = "enquiries/update_form.html"
    context_object_name = "enquiry"
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

    def get_context_data(self, **kwargs):
        context = super(EnquiryUpdateView, self).get_context_data()
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        context["states"] = get_states_only(file_path)
        return context


class EnquiryDeleteView(LoginRequiredMixin, View):

    def get(self, request, slug):
        prop_obj = Enquiry.objects.filter(slug=slug)
        prop_obj.delete()
        return HttpResponse("<script type=text/javascript>toastr.success('Enquiry deleted successfully')</script>")


def enquiry_delete_view(request, slug):
    prop_obj = Enquiry.objects.filter(slug=slug)
    prop_obj.delete()
    return HttpResponse("<script type=text/javascript>toastr.success('Enquiry deleted successfully')</script>")


class MyEnquiries(View):
    template_name = "enquiries/my_enquiries.html"

    def get(self, request):
        enquiries = Enquiry.objects.filter(from_user=self.request.user)
        context = {
            "enquiries": enquiries,
        }
        return render(request, self.template_name, context)


class MyEnquiryList(View):
    template_name = "enquiries/my_list_htmx.html"

    def get(self, request):
        enquiries = Enquiry.objects.filter(from_user=self.request.user)
        context = {
            "enquiries": enquiries,
        }
        return render(request, self.template_name, context)


class AgentEnquiryList(View):
    template_name = "enquiries/agent_enquiry_list.html"

    def get(self, request):
        user = self.request.user
        enquiries = Enquiry.objects.filter(to_agent=user.agent)
        context = {
            "enquiries": enquiries,
        }
        return render(request, self.template_name, context)


class GetStateCities(View):
    template_name = "enquiries/create_form.html"

    def post(self, request):
        state = request.POST['state']
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        cities = get_cities_only(file_path, state)
        data = {
            "cities": cities,
            "success": "request was successful cities populated..."
        }
        return JsonResponse(data=data, safe=False)
