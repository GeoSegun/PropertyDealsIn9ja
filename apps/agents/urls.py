from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    # path('upload_file/', csrf_exempt(views.upload_file), name="upload_file"),
    path('my_reviews/', views.GetMyReviews.as_view(), name="my_reviews"),
    # path('my_agency_reviews/', views.GetMyAgencyReviews.as_view(), name="my_agency_reviews"),
    # path('my_property_reviews/', views.GetMyPropertyReviews.as_view(), name="my_property_reviews"),
    path('filter_agents/', csrf_exempt(views.filter_agents), name="filter_agents"),
    path('ratings/<slug:slug>/', csrf_exempt(views.AgentReviewView.as_view()), name='agent_ratings'),
    path('create/', csrf_exempt(views.AgentCreateView.as_view()), name='create'),
    path('get_cities/', csrf_exempt(views.GetStateCities.as_view()), name="get_cities"),
    path('<slug:slug>/', views.AgentDetailView.as_view(), name='detail'),
    path('', views.AgentListView.as_view(), name='list'),
]
