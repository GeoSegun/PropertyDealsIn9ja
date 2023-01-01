from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_user(self, email, username, full_name, phone, password, **extra_fields):
        if not email:
            raise ValueError(_('User must provide email address'))
        email = self.normalize_email(email)
        self.email_validator(email)
        if not username:
            raise ValueError(_('User must provide username'))
        if not full_name:
            raise ValueError(_('Please provide your full name'))
        if not phone:
            raise ValueError(_('Please provide your phone number'))
        user = self.model(
            email=email,
            username=username,
            full_name=full_name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, phone, password, **extra_fields):
        if not password:
            raise ValueError(_('Superuser must have a password'))
        if not email:
            raise ValueError(_('Admin must provide email address'))
        email = self.normalize_email(email)
        self.email_validator(email)
        user = self.create_user(
            email,
            username,
            full_name,
            phone,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
