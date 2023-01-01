from django.urls import path
from apps.accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('set-new-password/<uidb64>/<token>/', views.CompletePasswordResetView.as_view(), name='reset-user-password'),
    path('reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),
]

htmx_urlpatterns = [
    path('check_username/', views.check_username, name="check_username"),
    path('check_email/', views.check_email, name="check_email"),
    path('check_phone/', views.check_phone, name='check_phone'),
    path('check_password/', views.check_password, name="check_password"),
]

urlpatterns += htmx_urlpatterns
