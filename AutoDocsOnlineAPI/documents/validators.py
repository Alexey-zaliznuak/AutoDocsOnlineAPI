from django.conf import settings
from django.core import validators


def validate_name_in_document(value):
    """
    Check prefix, postfix and valid characters
    """
    prefix = settings.TEMPLATE_NAME_IN_DOCUMENT_PREFIX
    postfix = settings.TEMPLATE_NAME_IN_DOCUMENT_POSTFIX

    message = (
        "Enter a valid name in document. This value may contain only letters "
        "and '-'/'_' characters and start/end with "
        f"'{prefix}' and '{postfix}' respectively."
    )
    regex = rf"^{prefix}[a-zA-Z-_]+{postfix}\Z"

    return validators.RegexValidator(regex, message)(value)
