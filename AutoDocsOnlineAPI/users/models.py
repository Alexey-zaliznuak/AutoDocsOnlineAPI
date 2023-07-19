from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        max_length=settings.USER_EMAIL_MAX_LENGTH,
        unique=True
    )
    email_confirmed = models.BooleanField(_("email confirmed"), default=False)
    confirmation_code = models.CharField(
        _("confirm code"),
        max_length=settings.CONFIRM_CODE_LENGHT,
        blank=True,
        null=True,
    )

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('uncorrect username')

        if self.is_staff:
            self.email_confirmed = True

    class Meta:
        ordering = ["-id"]
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email + " " + self.username + " " + str(self.pk)
