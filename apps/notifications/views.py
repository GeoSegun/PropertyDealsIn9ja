from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.notifications.models import Notification


@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(to_user=request.user, is_seen=False).order_by('-created_at')
    notification = Notification.objects.filter(to_user=request.user, is_seen=False)
    notification.update(is_seen=True)

    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/notification_list.html', context)


def notification_delete_view(request, pk):
    notifications = None
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(to_user=request.user, is_seen=False).order_by('-created_at')
        Notification.objects.filter(pk=pk, to_user=request.user, is_seen=False).delete()
    return {'notifications': notifications}


# def user_notification_delete_view(request, pk):
#     user = request.user
#     notification = Notification.objects.filter(pk=pk, to_user=user)
#     notification.update(is_seen=True)
#     return redirect('notifications:list')


def notification_counts(request):
    notifications = None
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(to_user=request.user, is_seen=False).order_by('-created_at')
        notification = Notification.objects.filter(to_user=request.user, is_seen=False)
        notification.update(is_seen=True)
    return {
        'notifications': notifications
    }
