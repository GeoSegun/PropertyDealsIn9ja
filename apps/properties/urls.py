from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    # path('upload_file/', csrf_exempt(views.upload_file), name="upload_file"),
    path('comments/<slug:slug>/', csrf_exempt(views.PropertyCommentView.as_view()), name='property_comments'),
    path('dashboard/', views.PropertyDashBoard.as_view(), name='property_dashboard'),
    path('create/', csrf_exempt(views.PropertyCreateView.as_view()), name='create'),
    path('edit/<slug:slug>/', views.PropertyUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', views.property_delete_view, name='delete'),
    path('get_cities/', csrf_exempt(views.GetStateCities.as_view()), name="get_cities"),
    path('favourite_list/', views.MyFavouriteListPropertyView.as_view(), name="get_favourites"),
    path('my_property_list/', views.MyListedProperties.as_view(), name="get_my_property_list"),
    path('add_favorite/', csrf_exempt(views.AddFavoriteProperty.as_view()), name='add_favorite'),
    path('remove_favorite/<slug:slug>/', csrf_exempt(views.RemoveFavoriteProperty.as_view()), name='remove_favorite'),
    path('<slug:slug>/', views.PropertyDetailView.as_view(), name='detail'),
    path('', views.PropertyListView.as_view(), name='list'),
]