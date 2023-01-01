from datetime import datetime
import humanize
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from apps.accounts.models import User
from apps.inboxes.models import InboxMessage


class InboxMessageView(LoginRequiredMixin, View):
    template_name = "inboxes/lobby.html"

    def get(self, request, **kwargs):
        user = request.user
        messages = InboxMessage.get_messages(user=user)
        active_direct = None
        directs = None

        if messages:
            message = messages[0]
            active_direct = message['user']
            directs = InboxMessage.objects.filter(user=user, msg_receiver=message['user'])
            directs.update(is_seen=True)

            for msg in messages:
                if msg["user"].username == active_direct.username:
                    msg['unread'] = 0
        context = {
            'directs': directs,
            'messages': messages,
            'active_direct': active_direct,
        }
        return render(request, self.template_name, context)


class DirectMessage(View):
    template_name = "inboxes/lobby.html"

    def get(self, request, username, **kwargs):
        user = request.user
        msgs = InboxMessage.get_messages(user=user)
        active_direct = User.objects.get(username=username)
        directs = InboxMessage.objects.filter(user=user, msg_receiver__username=username)
        directs.update(is_seen=True)

        for msg in msgs:
            if msg['user'].username == username:
                msg['unread'] = 0
        context = {
            'directs': directs,
            'messages': msgs,
            'active_direct': active_direct,
        }
        return render(request, self.template_name, context)

    # Send Direct message to user
    def post(self, request, **kwargs):
        from_user = self.request.user
        to_user_username = request.POST.get('to_user')
        print(to_user_username)
        msg = request.POST.get('message')
        to_user = User.objects.get(username=to_user_username)
        InboxMessage.send_message(from_user, to_user, msg)
        # return render(request, self.template_name)
        return HttpResponse(f'''
        <li class="media reply first" id="reply_msg">
            <div class="media-body text-right">
                <div class="date_time">{humanize.naturaltime(datetime.now())}</div>
                <p>{msg}</p>
            </div>
        </li>''')
        # context_data = {
        #     "success_msg": "Message sent!",
        #     "message": msg,
        #     "time_sent": datetime.now()
        # }
        # return JsonResponse(data=context_data, safe=False)


class SendDirectMessage(View):
    template_name = "inboxes/lobby.html"

    # Send Direct message to user
    def post(self, request, **kwargs):
        from_user = request.user
        to_user_username = request.POST.get('to_user')
        print(to_user_username)
        msg = request.POST.get('message')
        to_user = User.objects.get(username=to_user_username)
        InboxMessage.send_message(from_user, to_user, msg)
        # return render(request, self.template_name)
        return HttpResponse(f"<script type=text/javascript>toastr.success('Message sent successfully')</script>")

    # Send Direct message to user
    # def post(self, request, **kwargs):
    #     from_user = self.request.user
    #     to_user_username = request.POST.get('to_user')
    #     msg = request.POST.get('message')
    #     to_user = User.objects.get(username=to_user_username)
    #     InboxMessage.send_message(from_user, to_user, msg)
    #     print(to_user_username)
    #     msgs = InboxMessage.get_messages(user=from_user)
    #     context_data = {
    #         "success_msg": "Message sent!",
    #         "messages": msgs,
    #     }
    #     return JsonResponse(data=context_data, safe=False)
    #     # context = {
    #     #     "messages": msgs,
    #     # }
    #     # messages.success(request, "Message sent successfully")
    #     # return render(request, self.template_name, context)
    #     # return HttpResponse("<script type=text/javascript>toastr.success('Message sent successfully')</script>")

