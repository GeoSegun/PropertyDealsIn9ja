from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('delete/<slug:slug>/', csrf_exempt(views.enquiry_delete_view), name='delete'),
    path('edit/<slug:slug>/', views.EnquiryUpdateView.as_view(), name='update'),
    path('get_cities/', csrf_exempt(views.GetStateCities.as_view()), name="get_cities"),
    path('create/', csrf_exempt(views.EnquiryCreateView.as_view()), name='create'),
    path('my_enquiry_list/', views.MyEnquiryList.as_view(), name='my_enquiry_list'),
    path('agent_enquiry_list/', views.AgentEnquiryList.as_view(), name='agent_enquiry_list'),
    path('my_enquiries/', views.MyEnquiries.as_view(), name='my_enquiries'),
    path('<slug:slug>/payment/', views.EnquiryPaymentView.as_view(), name='payment'),
    path('<slug:slug>/', views.EnquiryDetailView.as_view(), name='detail'),
    path('', views.EnquiryListView.as_view(), name='list'),
]
