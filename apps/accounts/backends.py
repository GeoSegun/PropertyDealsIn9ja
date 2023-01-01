from django.contrib.auth import get_user_model
from django.utils import timezone


class MyBackend:

    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            user.last_online = timezone.now()  # At the request of the user, we will update the date and time of the last visit
            user.save(update_fields=['last_visit'])
            return user
        except get_user_model().DoesNotExist:
            return None

# {% if user.is_online %}
#     <div class="online"></div>
# {% endif %}
# <span class="text-muted">{{ user_profile.get_online_info }}</span>
