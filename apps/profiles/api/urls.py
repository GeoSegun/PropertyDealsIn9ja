from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.ProfileAPIView.as_view(), name='get_profile'),
    path('update/<str:username>/', views.ProfileUpdateAPIView.as_view(), name='update_profile'),
]
