from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    # path('select_currency/', csrf_exempt(views.select_currency), name='select_currency'),
    path('<slug:slug>/', csrf_exempt(views.ProfileView.as_view()), name='profile_detail'),
    path('update/<slug:slug>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('get_cities/<slug:slug>/', csrf_exempt(views.GetStateCities.as_view()), name="get_cities"),
]
