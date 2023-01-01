from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.notifications.views import notification_list_view, notification_delete_view

urlpatterns = [
    path('', notification_list_view, name="list"),
    path('<int:pk>/delete', csrf_exempt(notification_delete_view), name="delete"),
]
