from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from apps.contacts.models import Contact
from propertyDealsIn9ja import settings


class ContactView(View):
    template_name = "contact.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.user.is_authenticated:
            _name = request.user.username
            _email = request.user.email
            _phone = request.user.phone
        else:
            _name = request.POST['name']
            _email = request.POST['email']
            _phone = request.POST['phone']
        _message = request.POST['message']
        subject = request.POST['subject']
        context = {'message': _message, 'subject': subject, 'name': _name}
        email_template = render_to_string('includes/support_email.html', context)
        try:
            send_mail = EmailMessage(
                "Message for propertyDealsIn9ja.com",
                email_template,
                _email,
                [settings.SUPPORT_EMAIL],
            )
            send_mail.fail_silently = False
            send_mail.send()
            messages.success(request, "Email sent successfully...")
            return render(request, self.template_name)
        except Exception:
            contact = Contact.objects.create(
                name=_name,
                email=_email,
                phone=_phone,
                subject=subject,
                message=_message,
            )
            contact.save()
            messages.success(request, "Message sent and received successfully...")
            return render(request, self.template_name)
