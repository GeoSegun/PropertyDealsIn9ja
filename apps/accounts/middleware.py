import datetime

from django.core.cache import cache
from django.utils.timezone import now
from apps.accounts.models import User


class LastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            user = User.objects.get(id=request.user.id)
            user.last_visit = now()
            user.save(update_fields=['last_visit'])
        return self.get_response(request)


# class ActiveUserMiddleware:
#
#     def process_request(self, request):
#         current_user = request.user
#         if request.user.is_authenticated():
#             time_now = datetime.datetime.now()
#             cache.set(f"seen_{current_user.username}, {time_now}")
