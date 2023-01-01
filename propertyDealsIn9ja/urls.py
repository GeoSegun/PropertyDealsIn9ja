from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from propertyDealsIn9ja.settings import DEBUG
from propertyDealsIn9ja.views import HomeView, filter_property

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', csrf_exempt(HomeView.as_view()), name='home'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include(('apps.accounts.urls', 'apps.accounts'), namespace='accounts')),
    path('api/accounts/', include(('apps.accounts.api.urls', 'apps.accounts'), namespace='api_accounts')),
    path('social-auth', include('social_django.urls', namespace='social')),
    path('profiles/', include(('apps.profiles.urls', 'apps.profiles'), namespace='profiles')),
    path('api/profiles/', include(('apps.profiles.api.urls', 'apps.profiles'), namespace='profiles_api')),
    path('contacts/', include(('apps.contacts.urls', 'apps.contacts'), namespace="contacts")),
    path('agents/', include(('apps.agents.urls', 'apps.agents'), namespace="agents")),
    path('properties/', include(('apps.properties.urls', 'apps.properties'), namespace="properties")),
    path('enquiries/', include(('apps.enquiries.urls', 'apps.enquiries'), namespace="enquiries")),
    path('wallets/', include(('apps.wallets.urls', 'apps.wallets'), namespace="wallets")),
    path('chats/', include(('apps.chats.urls', 'apps.chats'), namespace='chats')),
    path('inbox/', include(('apps.inboxes.urls', 'apps.inboxes'), namespace='inboxes')),
    path('notifications/', include(('apps.notifications.urls', 'apps.notifications'), namespace='notifications')),
    path('filter_property/', csrf_exempt(filter_property), name='filter_property'),

]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='404.html'))]

admin.site.site_header = "PropertyDealsIn9ja Admin"
admin.site.site_title = "PropertyDealsIn9ja Admin Portal"
admin.site.site_title = "Welcome to the PropertyDealsIn9ja administration"
