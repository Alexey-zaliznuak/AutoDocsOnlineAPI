from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomUnicodeUsernameValidator(RegexValidator):
    regex = settings.USER_USERNAME_REGEX
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/-/_ characters.'
    )
    flags = 0
