import json
from os import stat
import os.path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View
from tinify import tinify

from apps.profiles.models import Profile
from apps.wallets.models import Wallet
from propertyDealsIn9ja.utils import get_states, get_states_only, get_cities_only


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = "profiles/profile.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.request.user.profile.slug)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context["user"] = self.request.user
        return context


class GetStateCities(View):
    template_name = "profiles/profile_update.html"
        
    def post(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        state = request.POST['state']
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        print(f"state from frontend {state}")
        cities = get_cities_only(file_path, state)
        print(cities)
        
        data = {
            "cities": cities,
            "success": "request was successful cities populated..."
        }
        return JsonResponse(data=data, safe=False)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profiles/profile_update.html"
    context_object_name = 'profile'
    fields = (
        "gender",
        "bio",
        "image",
        "country",
        "city",
        "state",
        "address",
        "birth_day",
    )

    def get_object(self, queryset=None):
        return Profile.objects.get(slug=self.kwargs.get("slug"))
    
    def form_valid(self, form, *args, **kwargs):
        profile_inst = form.save(commit=False)
        state = self.request.POST.get("state")
        city = self.request.POST.get("city")
        print(state, city)
        profile_inst.state = state
        profile_inst.city = city
        if profile_inst.image:
            print(profile_inst.image)
        #     source = tinify.from_file(profile_inst.image).to_file(profile_inst.image)
        #     profile_inst.image = source
        profile_inst.save()
        messages.success(self.request, "Profile updated successfully...")
        return super(ProfileUpdateView, self).form_valid(form)
    
    # def post(self, request, **kwargs):
    #     state = self.request.POST.get("state")
    #     city = self.request.POST.get("city")
    #     print(state, city)
    #     profile = Profile.objects.get(slug=self.kwargs.get("slug"))
    #     profile.state = state
    #     profile.city = city
    #     profile.save(update_fields=['state', 'city'])
    #     messages.success(request, "Profile updated successfully...")
    #     return redirect("profiles:profile_detail", self.request.user.profile.slug)
    
    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data()
        file_path = "propertyDealsIn9ja/states-and-cities.json"
        context['states'] = get_states_only(file_path)
        context["user"] = Profile.objects.get(user=self.request.user)
        return context
