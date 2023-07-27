from django.conf import settings
from django.core.exceptions import ValidationError


def name_in_document_validator(value) -> None:
    prefix = settings.TEMPLATE_NAME_IN_DOCUMENT_PREFIX
    postfix = settings.TEMPLATE_NAME_IN_DOCUMENT_POSTFIX

    if not value.startswith(prefix):
        raise ValidationError(
            f"Name in document must start with '{prefix}'"
        )

    if not value.endswith(postfix):
        raise ValidationError(
            f"Name in document must end with '{postfix}'"
        )
