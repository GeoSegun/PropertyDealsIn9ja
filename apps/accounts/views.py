import json
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from django.views.generic.base import View
from validate_email import validate_email

from apps.accounts.models import User
from apps.accounts.tokens import account_activation_token


def check_username(request):
    username = request.POST.get('username')
    if not str(username).isalnum():
        return HttpResponse("<small class='text-warning'>Username should contain alphanumeric characters.</small>")
    if User.objects.filter(username=username).exists():
        return HttpResponse("<small class='text-danger'>Sorry username already in use.</small>")
    return HttpResponse("<small class='text-success'>Username is available.</small>")


def check_email(request):
    email = request.POST.get('email')
    if not validate_email(email):
        return HttpResponse("<small class='text-warning'>Wrong email address.</small>")
    if User.objects.filter(email=email).exists():
        return HttpResponse("<small class='text-danger'>Sorry email already in use.</small>")
    return HttpResponse("<small class='text-success'>Email is available.</small>")


def check_phone(request):
    phone = request.POST.get('phone')
    print(f"Checking Phone {phone}")
    if "+" not in phone:
        return HttpResponse("<small class='text-danger'>Please affix country code on your phone number eg(+2348031234567)</small>")
    if len(phone) > 14:
        return HttpResponse("<small class='text-danger'>Invalid phone number</small>")
    if User.objects.filter(phone=phone).exists():
        return HttpResponse("<small class='text-danger'>Sorry phone number already in use.</small>")
    return HttpResponse("<small class='text-success'>Phone number is available.</small>")


# class SelectCountryCurrency(View):
#     def post(self, request, slug):
#         data = json.loads(request.body)
#         country = data["countryVal"]
#         print(f"country from frontend {country}")
#         profile = Profile.objects.get(slug=slug)
#         wallet = Wallet.objects.get(user=profile.user)
#         if country == "NG":
#             wallet.currency = "NGN"
#             wallet.save()
#             print("currency saved...")
#             messages.success(request, "currency updated successfully...")
#             return redirect("profiles:profile_detail", profile.slug)
#         # ELSE assign US Dollars...
#         wallet.currency = "USD"
#         wallet.balance = wallet.balance/0.0014
#         wallet.save()
#         print("currency saved...")
#         messages.success(request, "currency updated successfully...")
#         return redirect("profiles:profile_detail", profile.slug)


def check_password(request):
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    if password == "" and password2 == "":
        return HttpResponse("<small class='text-warning'>Passwords are empty</small>")
    elif password == password2:
        return HttpResponse("<small class='text-success'>Passwords matched and OK!</small>")
    return HttpResponse("<small class='text-danger'>Password does not matched!!!</small>")


class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        # get user data
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        context = {
            'fieldValues': request.POST
        }
        # validate data
        if (
            not User.objects.filter(username=username).exists()
            and not User.objects.filter(email=email).exists()
        ):
            if password == password2:
                if len(password) < 6:
                    messages.error(request, "password is too short")
                    return render(request, 'accounts/signup.html', context)
                # else create user account but dont activate the user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    full_name=full_name,
                    phone=phone,
                    password=make_password(password)
                )
                user.set_password(password)
                user.is_active = True  # TODO change back to False once email is ok...
                user.save()
                # # -> getting Domain we are on...
                # domain = get_current_site(request).domain
                # # -> Encode uid
                # uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                # # -> Token
                # token = account_activation_token.make_token(user)
                # message = "confirm your registration"
                # # -> Relative Url to verification...
                # link = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token})
                # # ========== Send activation email to user ============
                # email_template = render_to_string(
                #     'accounts/account_activation_email.html',
                #     {'user': user.username, 'domain': domain, 'link': link, 'message': message}
                # )
                # send_mail = EmailMessage(
                #     'Activate your BennyDealz Account',
                #     email_template,
                #     settings.SUPPORT_EMAIL,
                #     [email],
                # )
                # send_mail.fail_silently = False
                # send_mail.send()

                # ============== send success message to user =============
                # messages.success(request, "Account Created!, Check your email to activate your account")
                # return render(request, 'accounts/signup.html', context)

                # ========== TODO Remove this code when email is setup =======
                auth.login(request, auth.authenticate(
                    email=email,
                    password=password,
                ))
                messages.success(request, "Account created and login successful!, please update you credentials")
                return redirect("profiles:profile_detail", slug=user.profile.slug)
                # ========== TODO Remove this code when email is setup =======
            messages.error(request, "Passwords does not match please check!")
            return redirect('accounts:signup')
        return render(request, 'accounts/signup.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # -> check if user have clicked on authentication token
            if not account_activation_token.check_token(user, token):
                return redirect("accounts:login" + "?message=" + "User already activated")

            # -> Activate user if activation token is clicked
            if user.is_active:
                return redirect("accounts:login")
            user.is_active = True
            user.save()

            # -> Display success message after activation
            messages.success(request, "Account activated successfully")
            return redirect("accounts:login")

        except Exception as ex:
            messages.error(request, "Email not delivered due to your Network, try again")
            return redirect("accounts:login")


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get('password')

        if email and password:
            user = auth.authenticate(email=email, password=password)

            if user:
                # Login in users if user account is active...
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username} login was successful...")
                    # This redirects user to previous page if not redirect user to home...
                    if request.POST.get('next') != '':
                        return redirect(request.POST.get('next'))
                    return redirect('home')
                # Display error message or redirect to login page.
                messages.info(request, 'Account is not active,please check your email')
                return render(request, 'accounts/login.html')

            messages.warning(request, 'Invalid credentials, try again!!!.')
            return redirect('accounts:login')

        messages.error(request, 'Please fill all fields')
        return render(request, 'accounts/login.html')


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully Logged out.")
        return super(LogoutView, self).get(request, *args, **kwargs)


class PasswordResetView(View):
    def get(self, request):
        return render(request, "accounts/reset-password.html")

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, "please supply a valid email")
            return render(request, 'accounts/reset-password.html', context)

        # -> getting Domain we are on...
        current_site = get_current_site(request).domain
        user = User.objects.filter(email=email)

        if user.exists():
            uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            link = reverse('accounts:reset-user-password', kwargs={'uidb64': uid, 'token': token})
            message = "reset your password"
            # ========== Send activation email to user ============
            email_template = render_to_string('accounts/account_activation_email.html',
                                              {'user': user[0].username, 'domain': current_site, 'link': link,
                                               'message': message})
            send_mail = EmailMessage(
                'Reset your AdieuLane account password',
                email_template,
                settings.SUPPORT_EMAIL,
                [email],
            )
            send_mail.fail_silently = True
            send_mail.send()
            messages.success(request, "We have sent a password reset link to your email")
            return render(request, 'accounts/reset-password.html', context)
        messages.info(request, "Email does not exist")
        return render(request, 'accounts/reset-password.html', context)


class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user):
                messages.info(request, "Password link is invalid, please request for a new password")
                return render(request, 'accounts/reset-password.html', context)
        except Exception as ex:
            return render(request, 'accounts/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Password do not match.")
            return render(request, 'accounts/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, "Password is too short.")
            return render(request, 'accounts/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully, you can login with your new password")
            return redirect('accounts:login')
        except Exception as ex:
            messages.info(request, "Something was wrong...")
            return render(request, 'accounts/set-new-password.html', context)
