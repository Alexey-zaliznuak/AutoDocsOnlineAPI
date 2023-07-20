from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        primary_key=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
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

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('uncorrect username')

        if self.is_staff:
            self.email_confirmed = True

    class Meta:
        ordering = ["username"]
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return ' '.join([self.username, self.email])
