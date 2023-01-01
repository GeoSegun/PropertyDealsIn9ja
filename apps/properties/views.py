from msilib.schema import Property
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from propertyDealsIn9ja.utils import get_states_only, get_cities_only
from .forms import PropertyForm, PropertyMediaForm
from .models import Property, Comment, PropertyMedia
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PropertyFilter
from ..agents.models import Agent
from ..notifications.models import Notification
from ..wallets.models import WalletTransaction


class PropertyListView(View):
    paginate_by = 6
    template_name = "properties/list.html"
    
    def get(self, request, *args, **kwargs):
        properties = Property.objects.all()
        # Calling Django Filter...
        property_filter = PropertyFilter(request.GET, queryset=properties)
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        states = get_states_only(file_path)
        # for p in properties:
        #     print(p.property_images.all())
        context = {
            'properties': property_filter.qs,
            'states': states,
            'form': property_filter.form,
        }
        return render(request, self.template_name, context)


class PropertyDashBoard(LoginRequiredMixin, View):
    template_name = "properties/dashboard.html"

    def get(self, request):
        total_view_count = 0
        user = self.request.user
        user_agent = Agent.objects.get(business_user=user)
        property_count = Property.objects.filter(uploaded_by=user_agent).count()
        favourite_count = user.profile.favorite_properties.all().count()
        property_qs = Property.objects.filter(uploaded_by=user_agent)
        visitors_review_count = user.agent.agent_review.all().count()
        # Display The agent recent notifications...
        notifications = Notification.objects.filter(to_user=request.user, is_seen=False).order_by('-created_at')
        notification = Notification.objects.filter(to_user=request.user, is_seen=False)
        notification.update(is_seen=True)
        for instance in property_qs:
            total_view_count += instance.views_count
        context = {
            "property_count": property_count,
            "favourite_count": favourite_count,
            "total_view_count": total_view_count,
            "notifications": notifications,
            "visitors_review_count": visitors_review_count,
        }
        return render(request, self.template_name, context)


class PropertyDetailView(View):
    template_name = "properties/detail.html"
    
    def get(self, request, slug):
        property_obj = get_object_or_404(Property, slug=slug)
        similar_properties = Property.objects.filter(property_type=property_obj.property_type)\
            .filter(property_status=property_obj.property_status)\
            .filter(state=property_obj.state).exclude(slug=property_obj.slug)
        featured_properties = Property.objects.filter(featured=True).exclude(slug=property_obj.slug)
        property_obj.views_count = property_obj.views_count + 1
        property_obj.save()
        context = {
            "property": property_obj,
            "similar_properties": similar_properties,
            "featured_properties": featured_properties,
        }
        return render(request, self.template_name, context)


class PropertyCommentView(View):
    template_name = "properties/comment_list.html"

    def post(self, request, slug):
        get_property = get_object_or_404(Property, slug=slug)
        comment_val = self.request.POST.get("comment")
        print(comment_val)
        comment = Comment.objects.create(
            property=get_property,
            by=request.user,
            content=comment_val,
        )
        get_property.property_comment.add(comment)
        comments = get_property.property_comment.all()
        context = {
            "comments": comments,
        }
        return render(request, self.template_name, context)


class PropertyCreateView(LoginRequiredMixin, View):
    template_name = "properties/form.html"
    upload_price = 500
    featured_price = 500

    def get(self, request):
        form = PropertyForm()
        img_form = PropertyMediaForm()
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        states = get_states_only(file_path)
        wallet = self.request.user.wallet
        context = {
            'wallet': wallet,
            'upload_price': self.upload_price,
            'featured_price': self.featured_price,
            'form': form,
            'states': states,
            'img_form': img_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PropertyForm(request.POST)
        img_form = PropertyMediaForm(request.FILES)
        state = self.request.POST.get("state")
        city = self.request.POST.get("city")
        my_files = self.request.FILES.getlist("file")
        wallet = self.request.user.wallet
        total_balance = 0
        if form.is_valid():
            f = form.save(commit=False)
            total_balance = self.upload_price
            # Update total_balance if featured button was clicked
            if f.featured:
                total_balance = self.upload_price + self.featured_price
            # Check for wallet balance and debit
            if wallet.balance >= total_balance:
                # Debit wallet but dont dave yet...
                wallet.balance = F('balance') - total_balance
                # Update form and save...
                f.uploaded_by = self.request.user.agent
                f.property_image = my_files[0]
                print(f"{my_files[0]} Saved successfully")
                del my_files[0]
                f.state = state
                f.city = city
                f.save()
                for mf in my_files:
                    img_doc = PropertyMedia.objects.create(
                        img_property=f,
                        property_image=mf,
                        uploaded_by=self.request.user
                    )
                    img_doc.save()
                # After saving the files then save wallet...
                wallet.save()
                # Update wallet transaction...
                wallet_transaction = WalletTransaction.objects.create(
                    wallet=wallet,
                    transaction_id=f.name[:6],
                    currency=wallet.currency,
                    amount=total_balance,
                    payment_status="successful",
                )
                wallet.wallet_transactions.add(wallet_transaction)
                messages.success(self.request, "Property added successfully")
                # return JsonResponse({'message': 'Property added successfully', 'status': 'success'}, status=200, safe=False)
                return redirect("properties:get_my_property_list")
            messages.error(self.request, "You currently have insufficient balance")
            return redirect("wallets:fund_wallet", wallet.uid)
        context = {
            'wallet': wallet,
            'featured_price': self.featured_price,
            'upload_price': total_balance,
            'form': form,
            'img_form': img_form,
        }
        messages.error(self.request, "You currently have insufficient balance")
        return render(request, self.template_name, context)


# def upload_file(request):
#     print(request.FILES.getlist('img_list'))
#     return JsonResponse("Ok", safe=False)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    featured_price = 500
    template_name = "properties/edit.html"
    context_object_name = 'property'
    fields = (
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
    )

    def get_page_title(self):
        obj = self.get_object()
        return f"Updated {obj.name}"

    def get_context_data(self, **kwargs):
        context = super(PropertyUpdateView, self).get_context_data()
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        context["states"] = get_states_only(file_path)
        wallet = self.request.user.wallet
        context["upload_price"] = 500
        context["featured_price"] = self.featured_price
        context["property"] = Property.objects.get(slug=self.kwargs.get("slug"))
        return context

    def form_valid(self, form):
        wallet = self.request.user.wallet
        agent = Agent.objects.get(business_user=self.request.user)
        state = self.request.POST.get("state")
        city = self.request.POST.get("city")
        print(state, city)
        # Debit wallet but dont dave yet...
        current_property = form.save(commit=False)
        # Update total_balance if featured button was clicked
        if current_property.featured and wallet.balance >= self.featured_price:
            wallet.balance = F('balance') - self.featured_price
            current_property.uploaded_by = agent
            current_property.uploaded_at = timezone.now()
            current_property.state = state
            current_property.city = city
            current_property.save()
            # After saving the files then save wallet...
            wallet.save()
            # Update wallet transaction...
            wallet_transaction = WalletTransaction.objects.create(
                wallet=wallet,
                transaction_id=f"Prop-{current_property.name[:6]}",
                currency=wallet.currency,
                amount=self.featured_price,
                payment_status="successful",
            )
            wallet.wallet_transactions.add(wallet_transaction)
        # If featured button is not clicked go ahead and save model.
        current_property.uploaded_by = agent
        current_property.uploaded_at = timezone.now()
        current_property.state = state
        current_property.city = city
        current_property.save()
        # After saving the files then save wallet...
        wallet.save()
        messages.success(self.request, "Property updated successfully...")
        if self.request.POST.get('next') != '':
            return redirect(self.request.POST.get('next'))
        return redirect('properties:get_my_property_list')


class PropertyDeleteView(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):
        prop_obj = Property.objects.filter(slug=slug)
        prop_obj.delete()
        return HttpResponse("<script type=text/javascript>toastr.success('Property deletes successfully')</script>")


def property_delete_view(request, slug, *args, **kwargs):
    prop_obj = Property.objects.filter(slug=slug)
    prop_obj.delete()
    return HttpResponse("<script type=text/javascript>toastr.success('Property deleted successfully')</script>")


class GetFeaturedProperties(View):
    paginate_by = 6
    templates = "properties/featured_list.html"

    def get(self, request):
        featured_properties = Property.objects.all().filter(featured=True)
        context = {"featured_properties": featured_properties}
        return render(request, self.templates, context)


class MyFavouriteListPropertyView(LoginRequiredMixin, View):
    paginate_by = 6
    template_name = "properties/favourite_list.html"

    def get(self, request):
        favourites_properties = self.request.user.profile.favorite_properties.all()
        context = {
            "favourites": favourites_properties
        }
        return render(request, self.template_name, context)


class MyListedProperties(LoginRequiredMixin, View):
    paginate_by = 6
    template_name = "properties/my_property_list.html"

    def get(self, request):
        my_uploaded_properties = self.request.user.agent.properties.all()
        context = {
            "my_properties": my_uploaded_properties
        }
        return render(request, self.template_name, context)


class AddFavoriteProperty(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'post':
            result = ""
            prop_id = int(request.POST.get('prop_id'))
            print(prop_id)
            property_obj = get_object_or_404(Property, id=prop_id)
            is_favourite = property_obj in request.user.profile.favorite_properties.all()
            if not is_favourite:
                request.user.profile.favorite_properties.add(property_obj)
                message = "Property added as your favourite successfully."
                result = "<i class='icon fa fa-heart text-white'></i>"
            else:
                request.user.profile.favorite_properties.remove(property_obj)
                message = "Property removed from your favourite successfully."
                result = "<i class='icon fa fa-heart-o text-white'></i>"
            return JsonResponse({'result': result, 'message': message})


class RemoveFavoriteProperty(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):
        property_obj = get_object_or_404(Property, slug=slug)
        user = request.user
        if property_obj in user.profile.favorite_properties.all():
            user.profile.favorite_properties.remove(property_obj)
            messages.success(request, "Property removed from your favourite successfully.")
        # return redirect("properties:list")
        next_page = request.POST.get('next', '/')
        return HttpResponseRedirect(next_page)


class GetStateCities(View):
    template_name = "properties/list.html"

    def post(self, request):
        state = request.POST['state']
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        cities = get_cities_only(file_path, state)
        data = {
            "cities": cities,
            "success": "request was successful cities populated..."
        }
        return JsonResponse(data=data, safe=False)


def property_category_counts(request):
    featured_properties = Property.objects.filter(featured=True)
    apartments = Property.objects.filter(property_type="Apartment").count()
    lands = Property.objects.filter(property_type="Land").count()
    bqs = Property.objects.filter(property_type="BQ").count()
    terraces = Property.objects.filter(property_type="Terrace").count()
    semi_detaches = Property.objects.filter(property_type="Semi Detached").count()
    fully_detaches = Property.objects.filter(property_type="Fully Detached").count()
    offices = Property.objects.filter(property_type="Office").count()
    warehouses = Property.objects.filter(property_type="Warehouse").count()
    commercials = Property.objects.filter(property_type="Commercial").count()
    others = Property.objects.filter(property_type="Other").count()
    context = {
        'featured_properties': featured_properties,
        'apartments': apartments,
        'lands': lands,
        'bqs': bqs,
        'terraces': terraces,
        'semi_detaches': semi_detaches,
        'fully_detaches': fully_detaches,
        'offices': offices,
        'warehouses': warehouses,
        'commercials': commercials,
        'others': others
    }
    return render(request, "", context)


# class PropertyCategoryView(ListView):
#     model = Property
#     template_name = "properties/category.html"

#     def get_queryset(self):
#         return Property.objects.filter(category=self.category)

#     def get_context_data(self, **kwargs):
#         context = super(PropertyCategoryView, self).get_context_data(**kwargs)
#         context['category'] = self.category
#         return context

# name = request.GET.get("name")
# price = request.GET.get("price")
# property_type = request.GET.get("property_type")
# property_status = request.GET.get("property_status")
# uploaded_by = request.GET.get("uploaded_by")
# no_bed_room = request.GET.get("no_bed_room")
# no_bath_room = request.GET.get("no_bath_room")
# state = request.GET.get("state")
# city = request.GET.get("city")
# if name:
#     print(name)
#     properties = properties.filter(name__icontains=name)
# if property_type:
#     print(property_type)
#     properties = properties.filter(property_type__iexact=property_type)
# if property_status:
#     print(property_status)
#     properties = properties.filter(property_status__iexact=property_status)
# if uploaded_by:
#     properties = properties.filter(uploaded_by__business_name__iexact=uploaded_by)
# if no_bed_room:
#     properties = properties.filter(no_bed_room__iexact=no_bed_room)
# if no_bath_room:
#     properties = properties.filter(no_bath_room__iexact=no_bath_room)
# if state:
#     properties = properties.filter(state__iexact=state)
# if city:
#     properties = properties.filter(city__iexact=city)
