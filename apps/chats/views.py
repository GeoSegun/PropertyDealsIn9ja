from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.accounts.models import User
from apps.chats.models import ChatModel


class ChatView(LoginRequiredMixin, View):
    def get(self, request):
        user_conversation_list = self.request.user.sender.all()
        context = {
            'user_conversation_list': user_conversation_list,
        }
        # return render(request, "chats/inbox_lobby.html", context)
        return render(request, "chats/chat_lobby.html", context)


class ChatPageView(LoginRequiredMixin, View):
    def get(self, request, username):
        current_user = self.request.user
        sender_user = User.objects.get(username=self.kwargs['username'])
        # ========================Adder sender and reciever to user conversation model=========================
        if sender_user not in current_user.profile.conversations.all():
            current_user.profile.conversations.add(sender_user)
        if current_user not in sender_user.profile.conversations.all():
            sender_user.profile.conversations.add(current_user)
        # ========================Dynamic room name generator=========================
        if len(str(current_user.username)) > len(str(sender_user.username)):
            thread_name = f"chat_{current_user.username}-{sender_user.username}"
        else:
            thread_name = f"chat_{sender_user.username}-{current_user.username}"
        # ========================Update message.is_seen from False to True=========================
        messages = ChatModel.objects.all().filter(thread_name=thread_name)
        for msg in messages:
            msg.is_seen = True
            msg.save()
        # =================================================
        user_conversation_list = current_user.sender.all()
        user_obj = User.objects.get(username=username)
        context = {
            'user_conversation_list': user_conversation_list,
            'user_obj': user_obj,
            'messages': messages,
        }
        # return render(request, "chats/inbox_lobby.html", context)
        return render(request, "chats/chat_msgs.html", context)


class EchoChat(View):
    template_name = "chats/chat.html"

    def get(self, request, **kwargs):
        context = {
            "me": self.request.user,
            "user": User.objects.get(username=self.kwargs.get("username"))
        }
        return render(request, self.template_name, context)