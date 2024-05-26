from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts_app.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    personal_number = models.CharField(_("personal number"), unique=True, max_length=11)
    full_name = models.CharField(_("full name"), max_length=300)
    birth_date = models.DateField(_("birth date"), null=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    role = models.CharField(
        _("role"),
        max_length=50,
        choices=[("librarian", "Librarian"), ("user", "User")],
        default="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("custom user")
        verbose_name_plural = _("custom users")

    def __str__(self):
        return self.email
