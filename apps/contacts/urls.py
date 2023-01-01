from django.urls import path
from apps.contacts import views

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact')
]
