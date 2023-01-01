from django.urls import path

from apps.chats import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat_lobby'),
    path('<str:username>/', views.ChatPageView.as_view(), name='chat'),
    path('echo_chat/<str:username>/', views.EchoChat.as_view(), name='echo_chat'),
]