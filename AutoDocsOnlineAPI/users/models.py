import uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        _('username'),
        max_length=settings.USER_USERNAME_MAX_LENGTH,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        _('first name'),
        max_length=settings.USER_FIRST_NAME_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=settings.USER_LAST_NAME_MAX_LENGTH,
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        max_length=settings.USER_EMAIL_MAX_LENGTH,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    email_confirmed = models.BooleanField(_("email confirmed"), default=False)
    confirmation_code = models.CharField(
        _("confirm code"),
        max_length=settings.CONFIRM_CODE_LENGHT,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["username"]
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('uncorrect username')

        return super().clean()

    def save(self, *args, **kwargs) -> None:
        if self.is_staff:
            self.email_confirmed = True

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return ' '.join([self.username, self.email])
